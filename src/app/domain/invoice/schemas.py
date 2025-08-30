from __future__ import annotations

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO

from app.db import models as m
from app.lib import dto

"""Invoice DTO with nested creations from child class"""
class InvoiceDTO(SQLAlchemyDTO[m.Invoice]):
    config = dto.config(
        max_nested_depth=1,
        exclude={"created_at", "updated_at","receipt"},
    )

class InvoiceCreateDTO(SQLAlchemyDTO[m.Invoice]):
    config = dto.config(
        max_nested_depth=1,
        exclude={"id", "created_at", "updated_at","receipt","signature_url"},
    )

class InvoiceUpdateDTO(SQLAlchemyDTO[m.Invoice]):
    config = dto.config(
        max_nested_depth=1,
        exclude={"id", "created_at", "updated_at","receipt"},
        partial=True,
    )


