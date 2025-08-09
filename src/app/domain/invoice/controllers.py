from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
from uuid import UUID
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from advanced_alchemy.service import OffsetPagination
from litestar import Controller, get, post, delete, patch
from litestar.params import Dependency, Parameter
from litestar.response import Response,File
from litestar.enums import RequestEncodingType
from sqlalchemy import ColumnElement, or_

from litestar.datastructures import UploadFile
from litestar.params import Body
import cloudinary.uploader

from app.db import models as m
from app.domain.accounts.guards import requires_active_user
from app.domain.invoice.services import InvoiceService
from app.lib.deps import create_service_dependencies
from . import urls
from .schemas import InvoiceDTO, InvoiceCreateDTO, InvoiceUpdateDTO

cloudinary.config(
        cloud_name="dqtudbhm1",
        api_key="281978128992832",
        api_secret="H1AS_rUqO-Cmak9YHQ3Pl1zyUJ8",
        secure=True  
    )
CLOUDINARY_URL="cloudinary://281978128992832:H1AS_rUqO-Cmak9YHQ3Pl1zyUJ8@dqtudbhm1"

if TYPE_CHECKING:
    from advanced_alchemy.filters import FilterTypes
    from litestar.dto import DTOData

"""To write controller methods,
declare tags, return DTO, and dependencies
In dependencies, usually declare create service dependencies and services name, then
key, load if necessary and filters
"""

class InvoiceController(Controller):
    tags = ["Invoices"]
    return_dto = InvoiceDTO

    dependencies = create_service_dependencies(
        InvoiceService,
        key="invoice_service",
        load=[m.Invoice.items],
        filters={
            "id_filter": UUID,
            "created_at": True,
            "updated_at": True,
            "sort_field": "invoice_date",
            "search": "invoice_number,customer_name,company_name",
        },
    )

    """
    List method: service name, filters, dependencies and usually return offsetpagination
    for the working function, use list_and_count, return schema
    """
    @get(path=urls.INVOICE_LIST, operation_id="ListInvoices")
    async def list_invoices(
        self,
        invoice_service: InvoiceService,
        search_term:str | None,
    ) -> OffsetPagination[m.Invoice]:
        
        filters:list[ColumnElement[bool]]=[]
        if search_term:
            filters.append(
                or_(
                    m.Invoice.invoice_number.ilike(f"%{search_term}%"),
                    m.Invoice.customer_name.ilike(f"%{search_term}%")
                )
            )

        results, total = await invoice_service.list_and_count(*filters)
        return invoice_service.to_schema(data=results, total=total, filters=filters)
    

    """
    Get method: service name, id and return model
    use get, return schema
    """
    @get(path=urls.INVOICE_DETAILS, operation_id="GetInvoice")
    async def get_invoice(
        self,
        invoice_service: InvoiceService,
        invoice_id: Annotated[UUID, Parameter(title="Invoice ID")],
    ) -> m.Invoice:
        db_obj = await invoice_service.get(invoice_id)
        return invoice_service.to_schema(db_obj)
    

    """        exclude={"id","create_at","updated_at"}

    Post method: service name, data passing with DTOData[model]
    use create, return schema
    """
    @post(
        path=urls.INVOICE_CREATE,
        operation_id="CreateInvoice",
        dto=InvoiceCreateDTO,
        guards=[requires_active_user],
    )
    async def create_invoice(
        self,
        invoice_service: InvoiceService,
        data: DTOData[m.Invoice],
    ) -> m.Invoice:
        db_obj = await invoice_service.create(data)
        return invoice_service.to_schema(db_obj)
    

    @patch(
        path=urls.INVOICE_UPDATE,
        operation_id="UpdateInvoice",
        dto=InvoiceUpdateDTO,
        guards=[requires_active_user],
    )
    async def update_invoice(
        self,
        invoice_service: InvoiceService,
        data: DTOData[m.Invoice],
        invoice_id: Annotated[UUID, Parameter(title="Invoice ID")],
    ) -> m.Invoice:
        invoice_instance: m.Invoice = data.create_instance()
        db_obj = await invoice_service.update(item_id=invoice_id, data=invoice_instance)
        return invoice_service.to_schema(db_obj)

    """
    Delete method: service name. id
    use delete
    """
    @delete(
        path=urls.INVOICE_DELETE,
        operation_id="DeleteInvoice",
        return_dto=None,
        guards=[requires_active_user],
    )
    async def delete_invoice(
        self,
        invoice_service: InvoiceService,
        invoice_id: Annotated[UUID, Parameter(title="Invoice ID")],
    ) -> None:
        await invoice_service.delete(invoice_id)

    def render_invoice_html(self, invoice_data: m.Invoice) -> str:
        base_dir = Path(__file__).parent.parent.parent / "domain" / "web" / "templates"
        env = Environment(loader=FileSystemLoader(str(base_dir))) #search the template
        template = env.get_template("invoice_template.html") #get template
        html_out = template.render(invoice=invoice_data, static_path="/assets") #render template
        return html_out

    """
    get invoice data and render html template
    """
    @get(path="/invoice/{invoice_id:uuid}/preview", operation_id="PreviewInvoice", return_dto=None)
    async def preview_invoice(
        self,            # Save URL to invoice
        invoice_service: InvoiceService,
        invoice_id: Annotated[UUID, Parameter(title="Invoice ID")],
    ) -> Response:
        invoice = await invoice_service.get(invoice_id)
        html = self.render_invoice_html(invoice)
        return Response(content=html, media_type="text/html")

    """
    render email template and send email
    """
    @post(path="/invoice/{invoice_id:uuid}/send", operation_id="SendInvoiceEmail")
    async def send_invoice_email_route(
        self,
        invoice_service: InvoiceService,
        invoice_id: Annotated[UUID, Parameter(title="Invoice ID")],
    ) -> dict:
        from .utils import send_invoice_email  

        invoice = await invoice_service.get(invoice_id)

        #render html invoice
        invoice_html = self.render_invoice_html(invoice)

        #wrap with email emplate
        email_template_path = Path(__file__).parent.parent / "web" / "templates" / "invoice_email_template.html"
        env = Environment(loader=FileSystemLoader(email_template_path.parent))
        template = env.get_template(email_template_path.name)

        #get final email template
        final_html = template.render(invoice=invoice, invoice_html=invoice_html)

        #send email
        send_invoice_email(
            to=invoice.customer_mail,  
            subject=f"Invoice #{invoice.invoice_number} from Neural Dev Co., LTD",
            html_body=final_html,
        )

        return {"message": "Invoice email sent"}
    

    """
    keep the invoice image in cloudinary
    data: send Upload File, Body with RequestEncodingType.MULTI_PART
    """
    @post(
    path="/invoice/{invoice_id:uuid}/signature",
    operation_id="UploadInvoiceSignature",
    )
    async def upload_invoice_signature(
        self,
        invoice_service: InvoiceService,
        invoice_id: Annotated[UUID, Parameter(title="Invoice ID")],
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
    ) -> dict:
        try:
            #upload the image with uploader.upload and store in the folder
            result = cloudinary.uploader.upload(data.file, folder="invoice_signatures")

            #update signature_url in invoice
            await invoice_service.update(
                item_id=invoice_id,
                data=m.Invoice(signature_url=result.get("secure_url")),
            )

            return {
                "message": "Signature saved",
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
            }
        except Exception as e:
            return {"error": str(e)}
        
    
        





