from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from app import config
from app.db.models.invoice import Invoice
from app.lib import dto

if TYPE_CHECKING:
    from litestar.dto import DTOData

class InvoiceDTO(SQLAlchemyDTO[Invoice]):
    config=dto.config(max_nested_depth=1)

class InvoiceCreateDTO(SQLAlchemyDTO[Invoice]):
    config=dto.config(max_nested_depth=0,exclude={"id","subtotal","vat","total_amount"})

class InvoiceUpdateDTO(SQLAlchemyDTO[Invoice]):
    config=dto.config(max_nested_depth=0,exclude={"id","subtotal","vat","total_amount"},partial=True)