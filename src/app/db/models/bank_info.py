from __future__ import annotations

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import UUIDAuditBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .invoice import Invoice


class BankInfo(UUIDAuditBase):
    __tablename__ = "bank_info"
    __table_args__ = {"comment": "Bank payment details for the invoice"}

    invoice_number: Mapped[str] = mapped_column(
        ForeignKey("invoice.invoice_number", ondelete="CASCADE"),
        nullable=False
    ) #Foreign key to the parent table
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    swift: Mapped[str] = mapped_column(String(50), nullable=False)
    account_number: Mapped[str] = mapped_column(String(50), nullable=False)

    invoice: Mapped[Invoice] = relationship(
        back_populates="bank_info",
        lazy="selectin"
    )
    