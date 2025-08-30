 <script lang="ts">
  import { browser } from "$app/environment"
  import toast from "svelte-french-toast"
  import type { API } from "../../api"
  import { createReceiptService, getAllReceiptService } from "../../services/receipt"
  import { onMount } from "svelte"
  import { getAllInvoiceService, getInvoiceByNumber } from "../../services/invoice"
  import { goto } from "$app/navigation"

  let token:string|null=null

  if(browser){
      token = localStorage.getItem("token")
  }

  let data:any=null
  let invoiceNumber:string=""

    let formData:API.ReceiptCreate.ResponseBody={
        invoiceNumber:"Select",
        receiptNumber:"",
        paymentDate:"",
        receiptDate:"",
        paymentStatus:"Select",
        paymentTotal:0
    }

    const handleSubmit=async(event:Event)=>{
        event.preventDefault()
        if(!token){
            toast.error("The user has not logged in, Please log in")
            return
        }
        try{
            const finalFormData={...formData,invoiceNumber:invoiceNumber}
            const res=await createReceiptService(finalFormData,token)
            if(res){
                toast.success("Receipt Created Successfully")
            }
            goto("/receipt")
        }catch(e:any){
            toast.error(e.message)
        }
    }

    const getNextReceiptId=(receipts:{receiptNumber:string}[]):string=>{
        console.log(receipts.length)
      if (!receipts.length) return "RCP-0000001";

      const max=receipts.reduce((maxNum,curr)=>{
        const num=parseInt(curr.receiptNumber.replace("RCP-",""),10)
        return num>maxNum?num:maxNum;
      },0)
      const next=max+1
      return `RCP-${next.toString().padStart(7,"0")}`;
    }

    onMount(()=>{
        const fetchInvoices=async()=>{
            if(!token){
                toast.error("The user has not logged in, Please log in")
                return
            }
            const res=await getAllInvoiceService(token)
            data=res.items || []
            const response=await getAllReceiptService(token,"")
            const nextId=getNextReceiptId(response.items)
            formData={...formData,receiptNumber:nextId}
        }
        fetchInvoices()

    })

    const handleSelect=async(e:Event)=>{
        try{
            if(!token){
                toast.error("The user has not logged in, Please log in")
                return
            }
            const invoice=await getInvoiceByNumber(token,formData.invoiceNumber)
            invoiceNumber=invoice.invoiceNumber
            const paymentAmount=invoice.totalAmount
            formData={...formData,paymentTotal:paymentAmount}
        }catch(e:any){
            toast.error(e.message)
        }
    }


 </script>
 
 <div class="p-6 w-full">
      <h2 class="text-2xl font-bold mb-4 text-center">Create Receipt</h2>
      <form onsubmit={handleSubmit} class="space-y-4 flex w-full justify-center">
        <div class="w-[45%] space-y-4">
          <div>
            <label for="invoiceNumber" class="block mb-1 font-medium">Invoice Number</label>
            <select name="invoiceNumber" onchange={handleSelect} bind:value={formData.invoiceNumber} class="w-full p-2 border rounded">
              <option value="Select">Select</option>
                {#each data as invoice}
                <option value={invoice.id}>{invoice.invoiceNumber}</option>
                {/each}
            </select>
          </div>

          <div>
            <label for="receiptNumber" class="block mb-1 font-medium">Receipt Number</label>
            <input
              name="receiptNumber"
              class="w-full p-2 border rounded"
              type="text"
              bind:value={formData.receiptNumber}
              required
            />
          </div>

          <div>
            <label for="paymentStatus" class="block mb-1 font-medium">Payment Status</label>
            <select name="paymentStatus" bind:value={formData.paymentStatus}  class="w-full p-2 border rounded">
              <option value="Select">Select</option>
              <option value="paid">Paid</option>
              <option value="unpaid">Unpaid</option>
            </select>
          </div>

          <div>
            <label for="receiptDate" class="block mb-1 font-medium">Receipt Date</label>
            <input
              name="receiptDate"
              class="w-full p-2 border rounded"
              bind:value={formData.receiptDate}
              type="date"
              required
            />
          </div>

          <div>
            <label for="paymentDate" class="block mb-1 font-medium">Payment Date</label>
            <input
              name="paymentDate"
              class="w-full p-2 border rounded"
              bind:value={formData.paymentDate}
              type="date"
              required
            />
          </div>

          <div>
            <label for="paymentTotal" class="block mb-1 font-medium">Payment Total</label>
            <input
              name="paymentTotal"
              class="w-full p-2 border rounded"
              type="number"
              bind:value={formData.paymentTotal}
              min="0"
              step="0.01"
            />
          </div>

          <button
            type="submit"
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Submit Receipt
          </button>
        </div>
      </form>
    </div>