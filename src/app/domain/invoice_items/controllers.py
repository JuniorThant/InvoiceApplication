from __future__ import annotations

from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from litestar import Controller, get, post, patch, delete
from litestar.params import Dependency, Parameter

from app.db.models.invoice_item import InvoiceItem
from app.domain.accounts.guards import requires_active_user, requires_active_user
from app.lib.deps import create_service_dependencies
from app.domain.invoice_items.services import InvoiceItemService
from app.domain.invoice_items.schemas import (
    InvoiceItemDTO,
    InvoiceItemCreateDTO,
    InvoiceItemUpdateDTO,
)
from app.domain.invoice_items import urls

if TYPE_CHECKING:
    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData

class InvoiceItemController(Controller):

    guards=[requires_active_user]
    dependencies=create_service_dependencies(
        InvoiceItemService,
        key="invoice_item_service",
        filters={
            "id_filter":UUID,
            "sort_field":"name",
            "search":"name,description"
        }
    )
    tags=["InvoiceItems"]
    return_dto=InvoiceItemDTO

 

