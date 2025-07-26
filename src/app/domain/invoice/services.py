from __future__ import annotations

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from app.db import models as m

__all__ = ("InvoiceService",)


class InvoiceService(SQLAlchemyAsyncRepositoryService[m.Invoice]):
    """Handles invoice operations with nested invoice items."""

    class Repository(SQLAlchemyAsyncRepository[m.Invoice]):
        model_type = m.Invoice

    repository_type = Repository
    match_fields = ["invoice_number"]


