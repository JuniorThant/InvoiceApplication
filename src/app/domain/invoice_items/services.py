from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db.models.invoice_item import InvoiceItem  # ✅ Explicit import


class InvoiceItemService(SQLAlchemyAsyncRepositoryService[InvoiceItem]):

    class Repository(SQLAlchemyAsyncRepository[InvoiceItem]):
        model_type = InvoiceItem

    repository_type = Repository


