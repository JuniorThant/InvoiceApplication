import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "@/contexts/AuthProvider"
import { API } from "@/types/api"
import { createReceiptService } from "@/services/receipt"

export default function CreateReceipt() {
  const { auth } = useAuth()
  const navigate = useNavigate()

  const [formData, setFormData] = useState<API.ReceiptCreate.ResponseBody>({
    invoiceNumber: "",
    receiptNumber: "",
    paymentDate: "",
    receiptDate: "",
    paymentStatus: "",
    paymentTotal: "",
  })

  const [message, setMessage] = useState("")

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!auth?.token) {
      setMessage("Unauthorized.")
      return
    }

    try {
      const finalFormData = {
        ...formData,
      }

      await createReceiptService(finalFormData, auth.token)
      setMessage("Receipt created successfully!")
      setTimeout(() => navigate("/receipt"), 1000)
    } catch (error: any) {
      setMessage(`Error creating receipt: ${error.message}`)
    }
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4 text-center">Create Receipt</h2>
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
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Receipt Number</label>
            <input
              name="receiptNumber"
              value={formData.receiptNumber}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="text"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Payment Status</label>
            <input
              name="paymentStatus"
              value={formData.paymentStatus}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="text"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Receipt Date</label>
            <input
              name="receiptDate"
              value={formData.receiptDate}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="date"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Payment Date</label>
            <input
              name="paymentDate"
              value={formData.paymentDate}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="date"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Payment Total</label>
            <input
              name="paymentTotal"
              value={formData.paymentTotal}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              type="number"
              min="0"
              step="0.01"
            />
          </div>

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Submit Receipt
          </button>
          {message ? <div>{message}</div> : ""}
        </div>
      </form>
    </div>
  )
}
