
from __future__ import annotations

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from decimal import Decimal

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from app.db import models as m
from litestar.dto import DTOData

__all__ = ("ReceiptService",)

class ReceiptService(SQLAlchemyAsyncRepositoryService[m.Receipt]):
     "Handles receipt operations with nested receipt items"

     class Repository(SQLAlchemyAsyncRepository[m.Receipt]):
          model_type=m.Receipt
        
     repository_type= Repository
     match_fields=["receipt_number"]