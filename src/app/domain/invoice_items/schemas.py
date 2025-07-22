from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from app.db.models.invoice_item import InvoiceItem  # ✅ Explicit model import
from app.lib import dto

if TYPE_CHECKING:
    from litestar.dto import DTOData


class InvoiceItemDTO(SQLAlchemyDTO[InvoiceItem]):
    config=dto.config(
        max_nested_depth=1,
        exclude={"create_at","updated_at"}
    )

class InvoiceItemCreateDTO(SQLAlchemyDTO[InvoiceItem]):
    config=dto.config(
        max_nested_depth=0,
        exclude={"id","created_at","updated_at","total"}
    )

class InvoiceItemUpdateDTO(SQLAlchemyDTO[InvoiceItem]):
    config=dto.config(
        max_nested_depth=0,
        exclude={"id","created_at","updated_at","total"},
        partial=True
    )