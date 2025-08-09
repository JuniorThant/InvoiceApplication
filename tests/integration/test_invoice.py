from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_invoice_create_with_noauth(client:"AsyncClient")->None:
    response=await client.post("/invoice")
    assert response.status_code==401

async def test_invoice_create(client: "AsyncClient", user_token_headers: dict[str, str]) -> None:
    payload = {
        "invoiceNumber": "INV-1009",
        "customerName": "Mr Kaung Zin Thant",
        "customerMail": "kaungzinthant12@gmail.com",
        "companyName": "Doe Ltd",
        "invoiceDate": "2025-07-24",
        "credit": "30 days",
        "dueDate": "2025-08-23",
        "remark": "Thanks for your business",
        "items": [
            {
                "invoiceItemId": "ITEM-001",
                "invoiceNumber": "INV-1009",
                "name": "Monitor",
                "description": "24-inch LED Monitor",
                "quantity": 1,
                "unitPrice": 100.00
            },
            {
                "invoiceItemId": "ITEM-002",
                "invoiceNumber": "INV-1009",
                "name": "Wireless Mouse",
                "description": "Ergonomic wireless mouse",
                "quantity": 2,
                "unitPrice": 10.00
            }
        ],
        "bankInfo": {
            "invoiceNumber": "INV-1009",
            "bankName": "DBS Bank",
            "swift": "DBSE9434",
            "accountNumber": "SA8433748878"
        }
    }

    response = await client.post("/invoice", headers=user_token_headers, json=payload)
    assert response.status_code == 201






