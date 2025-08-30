from __future__ import annotations

from decimal import Decimal

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from litestar.dto import DTOData

from app.db import models as m

__all__ = ("InvoiceService",)

VAT_PERCENTAGE = Decimal("0.07")

class InvoiceService(SQLAlchemyAsyncRepositoryService[m.Invoice]):
    """Handles invoice operations with nested invoice items."""

    class Repository(SQLAlchemyAsyncRepository[m.Invoice]):
        model_type = m.Invoice

    repository_type = Repository
    match_fields = ["invoice_number"]

    """
    Before invoice creation, the amount, subtotal, vat and total_amount will be calculated automatically
    """
    async def create(self, data: DTOData[m.Invoice]) -> m.Invoice:
            invoice_instance: m.Invoice = data.create_instance()

            #Calculate amount in each item
            for item in invoice_instance.items:
                item.amount = item.quantity * item.unit_price

            #Calculate subtotal
            subtotal = sum(item.amount for item in invoice_instance.items)
            invoice_instance.subtotal = subtotal

            #Calculate vat and total amount
            invoice_instance.vat = subtotal * VAT_PERCENTAGE
            invoice_instance.total_amount = invoice_instance.subtotal + invoice_instance.vat

            #add invoice instance
            return await self.repository.add(invoice_instance)






