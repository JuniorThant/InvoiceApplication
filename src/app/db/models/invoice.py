from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import String, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import UUIDAuditBase

if TYPE_CHECKING:
    from .invoice_item import InvoiceItem


class Invoice(UUIDAuditBase):
    __tablename__ = "invoice"
    __table_args__ = {"comment": "Invoice to the customer"}

    invoice_number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    customer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    invoice_date: Mapped[date] = mapped_column(Date, nullable=False)
    credit: Mapped[str] = mapped_column(nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    remark: Mapped[str] = mapped_column(String(100), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    vat: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    #use lazyload normally for one to many relationship
    items: Mapped[list[InvoiceItem]] = relationship(
        back_populates="invoice",
        cascade="all, delete-orphan",
        lazy="selectin"  
    )
