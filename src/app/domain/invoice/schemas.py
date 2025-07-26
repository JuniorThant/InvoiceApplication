from __future__ import annotations
from typing import TYPE_CHECKING

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from app.db import models as m
from app.lib import dto

if TYPE_CHECKING:
    from uuid import UUID

"""Invoice Item DTO, no nested creations here"""
class InvoiceItemDTO(SQLAlchemyDTO[m.InvoiceItem]):
    config = dto.config(
        max_nested_depth=0,
        exclude={"created_at", "updated_at"}
    )

class InvoiceItemCreateDTO(SQLAlchemyDTO[m.InvoiceItem]):
    config = dto.config(
        max_nested_depth=0,
        exclude={
            "id",
            "created_at",
            "updated_at",
        },
    )

class InvoiceItemUpdateDTO(SQLAlchemyDTO[m.InvoiceItem]):
    config = dto.config(
        max_nested_depth=0,
        exclude={
            "id",
            "invoice",
            "invoice_id",
            "created_at",
            "updated_at",
        },
        partial=True,
    )

"""Invoice DTO with nested creations from child class"""
class InvoiceDTO(SQLAlchemyDTO[m.Invoice]):
    config = dto.config(
        max_nested_depth=1, 
        exclude={"created_at", "updated_at"},
    )

class InvoiceCreateDTO(SQLAlchemyDTO[m.Invoice]):
    config = dto.config(
        max_nested_depth=1,  
        exclude={"id", "created_at", "updated_at"},
    )

class InvoiceUpdateDTO(SQLAlchemyDTO[m.Invoice]):
    config = dto.config(
        max_nested_depth=1,
        exclude={"id", "created_at", "updated_at"},
        partial=True,
    )
