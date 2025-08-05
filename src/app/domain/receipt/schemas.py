from __future__ import annotations
from typing import TYPE_CHECKING
from xml.etree.ElementInclude import include

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from app.db import models as m
from app.lib import dto

if TYPE_CHECKING:
    from uuid import UUID

"""Receipt DTO with nested creations from child class"""
class ReceiptDTO(SQLAlchemyDTO[m.Receipt]):
    config=dto.config(
        max_nested_depth=1,
        exclude={"created_at","updated_at"}
    )

class ReceiptCreateDTO(SQLAlchemyDTO[m.Receipt]):
    config=dto.config(
        max_nested_depth=1,
        exclude={"id","create_at","updated_at","invoice"}
    )
