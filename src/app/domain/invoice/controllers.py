from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from advanced_alchemy.service import OffsetPagination
from litestar import Controller, get, post, patch, delete
from litestar.params import Dependency, Parameter

from app.db import models as m
from app.domain.accounts.guards import requires_active_user
from app.domain.invoice.services import InvoiceService
from app.lib.deps import create_service_dependencies
from . import urls
from .schemas import InvoiceDTO, InvoiceCreateDTO, InvoiceUpdateDTO

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
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[m.Invoice]:
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

    """
    Post method: service name, data passing with DTOData[model]
    use create, return schema
    """
    @post(path=urls.INVOICE_CREATE, operation_id="CreateInvoice", dto=InvoiceCreateDTO, guards=[requires_active_user])
    async def create_invoice(
        self,
        invoice_service: InvoiceService,
        data: DTOData[m.Invoice],
    ) -> m.Invoice:
        db_obj = await invoice_service.create(data)
        return invoice_service.to_schema(db_obj)

    # @patch(path=urls.INVOICE_UPDATE, operation_id="UpdateInvoice", dto=InvoiceUpdateDTO, guards=[requires_active_user])
    # async def update_invoice(
    #     self,
    #     invoice_service: InvoiceService,
    #     data: DTOData[m.Invoice],
    #     invoice_id: Annotated[UUID, Parameter(title="Invoice ID")],
    # ) -> m.Invoice:
    #     db_obj = await invoice_service.update(item_id=invoice_id, data=data.create_instance())
    #     return invoice_service.to_schema(db_obj)

    """
    Delete method: service name. id
    use delete
    """
    @delete(path=urls.INVOICE_DELETE, operation_id="DeleteInvoice", return_dto=None, guards=[requires_active_user])
    async def delete_invoice(
        self,
        invoice_service: InvoiceService,
        invoice_id: Annotated[UUID, Parameter(title="Invoice ID")],
    ) -> None:
        _ = await invoice_service.delete(invoice_id)

