from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
from uuid import UUID
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from advanced_alchemy.service import OffsetPagination
from litestar import Controller, get, post, delete
from litestar.params import Dependency, Parameter
from litestar.response import Response
from sqlalchemy import ColumnElement,or_

from app.db import models as m
from app.domain.accounts.guards import requires_active_user
from .services import  ReceiptService
from app.lib.deps import create_service_dependencies
from . import urls
from .schemas import ReceiptCreateDTO, ReceiptDTO

if TYPE_CHECKING:
    from advanced_alchemy.filters import FilterTypes
    from litestar.dto import DTOData

"""To write controller methods,
declare tags, return DTO, and dependencies
In dependencies, usually declare create service dependencies and services name, then
key, load if necessary and filters
"""

class ReceiptController(Controller):
    tags=["Receipts"]
    return_dto=ReceiptDTO

    dependencies=create_service_dependencies(
        ReceiptService,
        key="receipt_service",
        filters={
            "id_filter":UUID,
            "created_at":True,
            "updated_at":True
        }
    )

    """
    List method:service name,filters,dependencies and usually return offsetpagination
    for the working function, use list_and_count, return schema
    """
    @get(path=urls.RECEIPT_LIST,operation_id="ListReceipts")
    async def list_receipts(
        self,
        receipt_service:ReceiptService,
        search_term:str | None,
        filters: Annotated[list[FilterTypes | ColumnElement[bool]], Dependency(skip_validation=True)]
    )->OffsetPagination[m.Receipt]:

        if search_term:
            filters.append(
                or_(
                    m.Receipt.receipt_number.ilike(f"%{search_term}%"),
                    m.Receipt.invoice_number.ilike(f"%{search_term}%"),
                    m.Receipt.invoice.has(m.Invoice.customer_name.ilike(f"%{search_term}%"))
                )
            )

        results,total=await receipt_service.list_and_count(*filters)
        return receipt_service.to_schema(data=results,total=total,filters=filters)

    """
    Post method:service name, data passing with DTOData[model]
    use create,return schema
    """
    @post(
        path=urls.RECEIPT_CREATE,
        operation_id="CreateReceipt",
        dto=ReceiptCreateDTO
    )
    async def create_receipt(
        self,
        receipt_service:ReceiptService,
        data:DTOData[m.Receipt],
    )->m.Receipt:
        db_obj=await receipt_service.create(data)
        return receipt_service.to_schema(db_obj)

    """
    Delete method: service name. id
    use delete
    """
    @delete(
        path=urls.RECEIPT_DELETE,
        operation_id="DeleteReceipt",
        return_dto=None,
        guards=[requires_active_user],
    )
    async def delete_receipt(
        self,
        receipt_service: ReceiptService,
        receipt_id: Annotated[UUID, Parameter(title="Receipt ID")],
    ) -> None:
        await receipt_service.delete(receipt_id)
    
    def render_receipt_html(self,receipt_data:m.Receipt)->str:
        base_dir=Path(__file__).parent.parent.parent/"domain"/"web"/"templates"
        env=Environment(loader=FileSystemLoader(str(base_dir)))
        template=env.get_template("receipt_template.html")
        html_out=template.render(receipt=receipt_data)
        return html_out

    """
    get receipt data and render html template
    """
    @get(path="/receipt/{receipt_id:uuid}/preview",operation_id="PreviewReceipt",return_dto=None)
    async def preview_receipt(
        self,
        receipt_service:ReceiptService,
        receipt_id:Annotated[UUID,Parameter(title="Receipt ID")],
    ) -> Response:
        receipt=await receipt_service.get(receipt_id)
        html=self.render_receipt_html(receipt)
        return Response(content=html,media_type="text/html")
    
    """
    render email template and send email
    """
    @post(path="/receipt/{receipt_id:uuid}/send",operation_id="SendReceiptEmail")
    async def send_receipt_email_route(
        self,
        receipt_service:ReceiptService,
        receipt_id:Annotated[UUID,Parameter(title="Receipt ID")]
    )->dict:
        from .utils import send_receipt_email

        receipt=await receipt_service.get(receipt_id)

        receipt_html=self.render_receipt_html(receipt)

        email_template_path=Path(__file__).parent.parent / "web" / "templates"/ "receipt_email_template.html"
        env=Environment(loader=FileSystemLoader(email_template_path.parent))
        template=env.get_template(email_template_path.name)

        final_html=template.render(receipt=receipt,receipt_html=receipt_html)

        if not receipt.invoice:
            raise ValueError(f"Receipt {receipt_id} has no associated invoice.")

        send_receipt_email(
            to=receipt.invoice.customer_mail,
            subject=f"Receipt #{receipt.receipt_number} from Neural Dev Co., LTD",
            html_body=final_html
        )

        return{"message":"Receipt Email Sent"}

