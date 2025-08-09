from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Date, Numeric, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import UUIDAuditBase
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from .invoice import Invoice

class PaymentEnum(PyEnum):

    PAID="paid"
    UNPAID="unpaid"

class Receipt(UUIDAuditBase):
    __tablename__="receipt"
    __table_args__={"comment":"Receipt to the customer"}

    invoice_number:Mapped[str]=mapped_column(
        ForeignKey("invoice.invoice_number",ondelete="CASCADE"),
        nullable=False
    )
    receipt_number:Mapped[str]=mapped_column(String,nullable=False,unique=True)
    payment_date:Mapped[date]=mapped_column(Date,nullable=False)
    receipt_date:Mapped[date]=mapped_column(Date,nullable=False)
    payment_status:Mapped[PaymentEnum]=mapped_column(Enum(PaymentEnum),nullable=False)
    payment_total:Mapped[float]=mapped_column(nullable=False)

    invoice:Mapped[Optional[Invoice]]=relationship(
        back_populates="receipt",
        lazy="selectin"
    )

