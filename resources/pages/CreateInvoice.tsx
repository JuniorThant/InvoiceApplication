import React, { useEffect, useState } from "react";
import { createInvoiceService, getAllInvoiceService } from "@/services/invoice";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthProvider";
import { API } from "@/types/api";

export default function CreateInvoice() {
  const { auth } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState<API.InvoiceCreate.RequestBody>({
    invoiceNumber: "",
    customerName: "",
    customerMail: "",
    companyName: "",
    invoiceDate: "",
    credit: "",
    dueDate: "",
    remark: "",
    items: [],
    bankInfo: {
      invoiceNumber: "",
      bankName: "",
      swift: "",
      accountNumber: ""
    }
  });

  const [bankData, setBankData] = useState({
    invoiceNumber: "",
    bankName: "",
    swift: "",
    accountNumber: ""
  });

  const [item, setItem] = useState({
    invoiceNumber: "",
    name: "",
    description: "",
    quantity: "",
    unitPrice: ""
  });

  const [itemsCount, setItemsCount] = useState<
    {
      invoiceNumber: string;
      name: string;
      description: string;
      quantity: number;
      unitPrice: number;
    }[]
  >([]);

  const [message, setMessage] = useState("");

  const getNextInvoiceId=(invoices:{invoiceNumber:string}[]):string=>{
    if(!invoices.length) return "INV-0000001";

    const max=invoices.reduce((maxNum,curr)=>{
      const num=parseInt(curr.invoiceNumber.replace("INV-",""),10);
      return num>maxNum?num:maxNum;
    },0)
    const next=max+1;
    return `INV-${next.toString().padStart(7,"0")}`;
  }

  useEffect(() => {
  const generateInvoiceId = async () => {
    try {
      if (!auth?.token) return;

      const res = await getAllInvoiceService(auth.token);
      const invoices = res.items || [];
      const nextId = getNextInvoiceId(invoices);

      setFormData((prev) => ({
        ...prev,
        invoiceNumber: nextId,
      }));

      setBankData((prev) => ({
        ...prev,
        invoiceNumber: nextId,
      }));
    } catch (err) {
      console.error("Failed to generate invoice number:", err);
    }
  };

  generateInvoiceId();
}, [auth?.token]);


  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
    setBankData((prev) => ({
      ...prev,
      invoiceNumber: formData.invoiceNumber
    }));
  };

  const handleBankChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setBankData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleItemChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setItem((prev) => ({
      ...prev,
      [name]: ["quantity", "unitPrice"].includes(name)
        ? value === "" ? "" : parseFloat(value)
        : value
    }));
  };

  const handleAddItem = () => {
    if (
      !item.name ||
      item.quantity === "" ||
      item.unitPrice === "" ||
      isNaN(Number(item.quantity)) ||
      isNaN(Number(item.unitPrice))
    ) {
      setMessage("Please fill all item fields before adding.");
      return;
    }

    setItemsCount((prev) => [
      ...prev,
      {
        invoiceNumber: formData.invoiceNumber,
        name: item.name,
        description: item.description,
        quantity: Number(item.quantity),
        unitPrice: Number(item.unitPrice)
      }
    ]);

    setItem({
      invoiceNumber: "",
      name: "",
      description: "",
      quantity: "",
      unitPrice: ""
    });

    setMessage("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!auth?.token) {
      setMessage("Unauthorized.");
      return;
    }

    try {
      const finalFormData = {
        ...formData,
        bankInfo: bankData,
        items: itemsCount
      };

      await createInvoiceService(finalFormData, auth.token);
      setMessage("Invoice created successfully!");
      setTimeout(() => navigate("/"), 1000);
    } catch (error: any) {
      setMessage(`Error creating invoice: ${error.message}`);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4 text-center">Create Invoice</h2>
      <form onSubmit={handleSubmit} className="space-y-4 flex w-full">
        <div className="w-[45%] space-y-4">
          <div>
            <label className="block mb-1 font-medium">Invoice Number</label>
            <input
              name="invoiceNumber"
              value={formData.invoiceNumber}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="text"
              required
              readOnly
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Customer Name</label>
            <input
              name="customerName"
              value={formData.customerName}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="text"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Customer Email</label>
            <input
              name="customerMail"
              value={formData.customerMail}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="email"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Company Name</label>
            <input
              name="companyName"
              value={formData.companyName}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="text"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Invoice Date</label>
            <input
              name="invoiceDate"
              value={formData.invoiceDate}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="date"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Credit Terms</label>
            <input
              name="credit"
              value={formData.credit}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="text"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Due Date</label>
            <input
              name="dueDate"
              value={formData.dueDate}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="date"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Remark</label>
            <textarea
              name="remark"
              value={formData.remark}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Bank Name</label>
            <input
              name="bankName"
              value={bankData.bankName}
              onChange={handleBankChange}
              className="w-full p-2 border rounded"
              type="text"
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Swift Number</label>
            <input
              name="swift"
              value={bankData.swift}
              onChange={handleBankChange}
              className="w-full p-2 border rounded"
              type="text"
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Account Number</label>
            <input
              name="accountNumber"
              value={bankData.accountNumber}
              onChange={handleBankChange}
              className="w-full p-2 border rounded"
              type="text"
            />
          </div>

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Submit Invoice
          </button>

          {message && <p className="text-red-600 text-sm mt-2">{message}</p>}
        </div>

        <div className="w-[10%]"></div>

        <div className="w-[45%] space-y-4">
          <h3 className="text-xl font-semibold">Add Invoice Item</h3>

          <div>
            <label className="block mb-1 font-medium">Item Name</label>
            <input
              name="name"
              value={item.name}
              onChange={handleItemChange}
              className="w-full p-2 border rounded"
              type="text"
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Description</label>
            <input
              name="description"
              value={item.description}
              onChange={handleItemChange}
              className="w-full p-2 border rounded"
              type="text"
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Quantity</label>
            <input
              name="quantity"
              value={item.quantity}
              onChange={handleItemChange}
              className="w-full p-2 border rounded"
              type="number"
              min="0"
              step="1"
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Unit Price</label>
            <input
              name="unitPrice"
              value={item.unitPrice}
              onChange={handleItemChange}
              className="w-full p-2 border rounded"
              type="number"
              min="0"
              step="0.01"
            />
          </div>

          <button
            type="button"
            onClick={handleAddItem}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Add Item
          </button>

          {itemsCount.length > 0 && (
            <div className="mt-4">
              <h4 className="font-semibold mb-2">Items Preview</h4>
              <ul className="space-y-2">
                {itemsCount.map((itm, idx) => (
                  <li key={idx} className="border p-2 rounded bg-gray-50">
                    <p>{itm.invoiceNumber}</p>
                    <p>
                      <strong>{itm.name}</strong> - {itm.quantity} × ${itm.unitPrice}
                    </p>
                    {itm.description && (
                      <p className="text-sm text-gray-600">{itm.description}</p>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </form>
    </div>
  );
}
