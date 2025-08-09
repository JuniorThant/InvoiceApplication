import React, { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "@/contexts/AuthProvider"
import { API } from "@/types/api"
import { createReceiptService, getAllReceiptService } from "@/services/receipt"
import { toast } from "sonner"
import { getAllInvoiceService, getInvoiceByNumber } from "@/services/invoice"

export default function CreateReceipt() {
  const { auth } = useAuth()
  const navigate = useNavigate()
  const [invoices, setInvoices] = useState<
    API.InvoiceList.Http200.InvoiceSummary[]
  >([])

  const [selectedValue,setSelectedValue]=useState('')

  const [formData, setFormData] = useState<API.ReceiptCreate.ResponseBody>({
    invoiceNumber: "",
    receiptNumber: "",
    paymentDate: "",
    receiptDate: "",
    paymentStatus: "",
    paymentTotal: "",
  })

  const [paymentFinal,setPaymentFinal]=useState(0)

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const fetchInvoices = async () => {
        if (!auth?.token) {
          toast("No auth token found. Please log in.")
          return
        }
  
        try {
          const data = await getAllInvoiceService(auth.token)

          setInvoices(data.items)
        } catch (e: any) {
          toast(`Failed to fetch invoices: ${e.message}`)
        } 
      }

  useEffect(()=>{
    fetchInvoices()
      const generateReceiptId = async () => {
        try {
          if (!auth?.token) return;
    
          const res = await getAllReceiptService(auth.token);
          const receipts = res.items || [];
          const nextId = getNextReceiptID(receipts);
    
          setFormData((prev) => ({
            ...prev,
            receiptNumber: nextId,
          }));
    
        } catch (err) {
          console.error("Failed to generate invoice number:", err);
        }
      };
    
      generateReceiptId();
  },[])

  const getNextReceiptID=(receipts:{receiptNumber:string}[]):string=>{
    if(!receipts.length)return "RCP-0000001"

    const max=receipts.reduce((maxNum,curr)=>{
      const num=parseInt(curr.receiptNumber.replace("RCP-",""),10)
      return num>maxNum?num:maxNum;
    },0)
    const next=max+1
    return `RCP-${next.toString().padStart(7,"0")}`
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!auth?.token) {
      toast("Unauthorized.")
      return
    }

    try {
      const finalFormData = {
        ...formData,
      }

      await createReceiptService(finalFormData, auth.token)
      toast("Receipt Create Successfully")
      setTimeout(() => navigate("/receipt"), 1000)
    } catch (error: any) {
      toast(`Error creating receipt: ${error.message}`)
    }
  }

  const handleSelect = async (e: React.ChangeEvent<HTMLSelectElement>) => {
  if (!auth?.token) {
    toast("Unauthorized")
    return
  }

  const selected = e.target.value
  setSelectedValue(selected)

  try {
    const invoice = await getInvoiceByNumber(auth.token, selected)
    const invoiceNumber=invoice.invoiceNumber
 
    const paymentAmount = invoice.totalAmount
    setPaymentFinal(paymentAmount)
       setFormData((prev) => ({
      ...prev,
      invoiceNumber: invoiceNumber,
      paymentTotal:paymentAmount.toString()
    }));
  } catch (err: any) {
    console.error("Failed to fetch invoice:", err.message)
    toast("Failed to fetch invoice.")
  }
}


  return (
    <div className="p-6 ">
      <h2 className="text-2xl font-bold mb-4 text-center">Create Receipt</h2>
      <form onSubmit={handleSubmit} className="space-y-4 flex w-full justify-center">
        <div className="w-[45%] space-y-4">
          <div>
            <label className="block mb-1 font-medium">Invoice Number</label>
            <select name="invoiceNumber" value={selectedValue} onChange={handleSelect} className="w-full p-2 border rounded">
              <option value="Select">Select</option>
              {invoices.map((invoice)=>(
                <option key={invoice.id} value={invoice.id}>{invoice.invoiceNumber}</option>
              ))}
            </select>
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
              readOnly
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Payment Status</label>
            <select name="paymentStatus" value={formData.paymentStatus} onChange={handleChange} className="w-full p-2 border rounded">
              <option value="select">Select</option>
              <option value="paid">Paid</option>
              <option value="unpaid">Unpaid</option>
            </select>
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
              value={paymentFinal}
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
        </div>
      </form>
    </div>
  )
}
