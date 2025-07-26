from __future__ import annotations

from decimal import Decimal
from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import UUIDAuditBase

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .invoice import Invoice


class InvoiceItem(UUIDAuditBase):
    __tablename__ = "invoice_item"
    __table_args__ = {"comment": "Line items belonging to an invoice"}

    invoice_number: Mapped[str] = mapped_column(
        ForeignKey("invoice.invoice_number", ondelete="CASCADE"),
        nullable=False
    ) #Foreign key to the parent table
    invoice_item_id: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), default=None)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    #use lazy load normally for one to many relationship
    invoice: Mapped[Invoice] = relationship(
        back_populates="items",
        lazy="selectin" 
    )
