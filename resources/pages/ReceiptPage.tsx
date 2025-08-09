import SideBar from "@/components/SideBar"
import { useAuth } from "@/contexts/AuthProvider"
import { deleteReceiptService, getAllReceiptService, sendReceiptEmailService } from "@/services/receipt"
import type { API } from "@/types/api"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"

export default function ReceiptPage() {
  const { auth } = useAuth()
  const [receipts, setReceipts] = useState<
    API.ReceiptList.Http200.ReceiptSummary[]
  >([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [modal, setModal] = useState(false)
  const [deleteModal, setDeleteModal] = useState(false)
    const [searchTerm,setSearchTerm]=useState("")
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState("");

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
    }, 500);

    return () => {
      clearTimeout(handler);
    };
  }, [searchTerm]);

  const fetchReceipts = async () => {
    if (!auth.token) {
      setError("The user has not logged in, Please log in")
      return
    }
    setLoading(true)
    try {
      const data = await getAllReceiptService(auth.token,debouncedSearchTerm)
      setReceipts(data.items)
    } catch (e: any) {
      setError(`Failed to fetch receipts: ${e.message}`)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchReceipts()
  }, [debouncedSearchTerm])

    const handleSendEmail = async (receiptId: string) => {
      if (!auth?.token) {
        setError("No auth token found. Please log in.")
        return
      }
  
      try {
        setLoading(true)
        await sendReceiptEmailService(receiptId, auth.token)
        toast("Email sent successfully")
      } catch (e: any) {
        console.error(e)
        alert(`Failed to send receipt email: ${e.message}`)
      } finally {
        setLoading(false)
      }
    }

  const navigate = useNavigate()
  const formatAmount = (amount: any) => {
    const num = Number(amount)
    if (isNaN(num)) return "0.00"
    return num.toFixed(2)
  }

  const handleDelete=async(id:string)=>{
    await deleteReceiptService(id,auth.token)
    toast("Receipt Deleted Successfully")
    fetchReceipts()
  }

  return (
    <div>
      <div className="flex">
        <SideBar />
        <div className="flex-1 ml-64 p-5">
          <button
            onClick={() => navigate("/create/receipt")}
            className="mb-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Create New Receipt
          </button>
          <div className="w-1/3"> 
          <input type="text" 
          className="w-full px-4 py-2 border rounded-md my-2"
          placeholder="Search Requests"
          value={searchTerm}
          onChange={(e)=>setSearchTerm(e.target.value)}
          />
          {searchTerm}
          </div>
          {modal && (
            <div className=" rounded-md p-3 w-[20%] top-[40%] left-[40%] z-10 absolute bg-white shadow-xl">
              <p>Email sent successfully!</p>
              <div className="flex justify-end">
                <button
                  className="button text-white bg-blue-600 rounded-md p-2"
                  onClick={() => setModal(false)}
                >
                  Okay
                </button>
              </div>
            </div>
          )}
          {deleteModal && (
            <div className=" rounded-md p-3 w-[20%] top-[40%] left-[40%] z-10 absolute bg-white shadow-xl text-red-500">
              <p>Invoice Deleted Successfully</p>
              <div className="flex justify-end">
                <button
                  className="button text-white bg-red-600 rounded-md p-2"
                  onClick={() => setDeleteModal(false)}
                >
                  Okay
                </button>
              </div>
              *
            </div>
          )}
          {loading && <p>Loading receipts...</p>}
          {error && <p className="text-red-600">{error}</p>}
          {!loading && !error && (
            <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
              <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                  <tr>
                    <th className="px-6 py-3">Receipt Number</th>
                    <th className="px-6 py-3">Invoice Number</th>
                    <th className="px-6 py-3">Payment Date</th>
                    <th className="px-6 py-3">Payment Status</th>
                    <th className="px-6 py-3">Total Amount</th>
                    <th className="px-6 py-3">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {receipts.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="px-6 py-4 text-center">
                        No receipts found.
                      </td>
                    </tr>
                  ) : (
                    receipts.map((receipt) => (
                      <tr
                        key={receipt.id}
                        className="odd:bg-white even:bg-gray-50 border-b dark:border-gray-700"
                      >
                        <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">
                          {receipt.receiptNumber}
                        </td>
                        <td className="px-6 py-4">{receipt.invoiceNumber}</td>
                        <td className="px-6 py-4">{receipt.paymentDate}</td>
                        <td className="px-6 py-4 capitalize">{receipt.paymentStatus}</td>
                        <td className="px-6 py-4">
                          ${formatAmount(receipt.paymentTotal)}
                        </td>
                        <td className="px-6 py-4 space-x-2">
                          <a
                            href={`/receipt/${receipt.id}/preview`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline"
                          >
                            View
                          </a>
                          <button
                            onClick={() => handleSendEmail(receipt.id)}
                            className="text-green-900 hover:underline"
                          >
                            Email
                          </button>
                          <button
                            onClick={() => handleDelete(receipt.id)}
                            className="text-red-700 hover:underline"
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
