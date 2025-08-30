<script lang="ts">

import type {API} from '../../api'
  import { createInvoiceService, getAllInvoiceService } from '../../services/invoice'
  import { browser } from '$app/environment';
  import { goto } from '$app/navigation'
  import toast from 'svelte-french-toast'
  import { onMount } from 'svelte'

 
    let token:string|null=null
    let formData:API.InvoiceCreate.RequestBody={
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
    }

    let bankData={
        invoiceNumber:"",
        bankName:"",
        swift:"",
        accountNumber:""
    }

    let item={
        invoiceNumber:"",
        name:"",
        description:"",
        quantity:0,
        unitPrice:0
    }

    let itemsCount:{
        invoiceNumber:string;
        name:string;
        description:string;
        quantity:number;
        unitPrice:number;
    }[]=[]

    let message:string=''

    const handleAddItem=()=>{
        if(
            !item.name ||
            item.quantity === 0 ||
            item.unitPrice === 0 ||
            isNaN(Number(item.quantity)) ||
            isNaN(Number(item.unitPrice))
        ){
            message="Plase fill all item fields before adding"
            return
        }

        itemsCount=[...itemsCount,{...item,invoiceNumber:formData.invoiceNumber}]

        item={
            invoiceNumber:formData.invoiceNumber,
            name:"",
            description:"",
            quantity:0,
            unitPrice:0
        }
    }

    if(browser){
   token=localStorage.getItem("token")
}
    const handleSubmit=async(event:Event)=>{

        if(!token){
            return
        }

        event.preventDefault()

        const finalBankData={...bankData,invoiceNumber:formData.invoiceNumber}
        const finalFormData={
            ...formData,
            bankInfo:finalBankData,
            items:itemsCount
        }
        const res=await createInvoiceService(finalFormData,token)
        if(res){
            toast.success("Invoice Created Successfully")
            goto("/invoice")
        }
    }

    const getNextInvoiceId=(invoices:{invoiceNumber:string}[]):string=>{
      if (!invoices.length) return "INV-0000001";

      const max=invoices.reduce((maxNum,curr)=>{
        const num=parseInt(curr.invoiceNumber.replace("INV-",""),10)
        return num>maxNum?num:maxNum;
      },0)
      const next=max+1
      return `INV-${next.toString().padStart(7,"0")}`;
    }

    onMount(()=>{
      const generateInvoiceId=async()=>{
        if(!token) return;
        const res=await getAllInvoiceService(token)
        const invoices=res.items || []
        const nextId=getNextInvoiceId(invoices)
        formData={...formData,invoiceNumber:nextId}
        console.log(formData)
      }
      generateInvoiceId()
    })

</script>

<div class="p-6 w-full">
      <h2 class="text-2xl font-bold mb-4 text-center">Create Invoice</h2>
      <form onsubmit={handleSubmit} class="space-y-4 flex w-full">
        <div class="w-[45%] space-y-4">
          <div>
            <label for="invoiceNumber" class="block mb-1 font-medium">Invoice Number</label>
            <input
              name="invoiceNumber"
              class="w-full p-2 border rounded"
              type="text"
              bind:value={formData.invoiceNumber}
              required
              readonly
            />
          </div>

          <div>
            <label for="customerName" class="block mb-1 font-medium">Customer Name</label>
            <input
              name="customerName"
              class="w-full p-2 border rounded"
              type="text"
              bind:value={formData.customerName}
              required
            />
          </div>

          <div>
            <label for="customerMail" class="block mb-1 font-medium">Customer Email</label>
            <input
              name="customerMail"
              class="w-full p-2 border rounded"
              type="email"
              bind:value={formData.customerMail}
              required
            />
          </div>

          <div>
            <label for="companyName" class="block mb-1 font-medium">Company Name</label>
            <input
              name="companyName"
              class="w-full p-2 border rounded"
              type="text"
              bind:value={formData.companyName}
              required
            />
          </div>

          <div>
            <label for="invoiceDate" class="block mb-1 font-medium">Invoice Date</label>
            <input
              name="invoiceDate"
              class="w-full p-2 border rounded"
              type="date"
              bind:value={formData.invoiceDate}
              required
            />
          </div>

          <div>
            <label for="credit" class="block mb-1 font-medium">Credit Terms</label>
            <input
              name="credit"
              class="w-full p-2 border rounded"
              type="text"
              bind:value={formData.credit}
              required
            />
          </div>

          <div>
            <label for="dueDate" class="block mb-1 font-medium">Due Date</label>
            <input
              name="dueDate"
              class="w-full p-2 border rounded"
              type="date"
              bind:value={formData.dueDate}
              required
            />
          </div>

          <div>
            <label for="remark" class="block mb-1 font-medium">Remark</label>
            <textarea
              name="remark"
              class="w-full p-2 border rounded"
              bind:value={formData.remark}
            ></textarea>
          </div>

          <div>
            <label for="bankName" class="block mb-1 font-medium">Bank Name</label>
            <input
              name="bankName"
              class="w-full p-2 border rounded"
              bind:value={bankData.bankName}
              type="text"
            />
          </div>

          <div>
            <label for="swift" class="block mb-1 font-medium">Swift Number</label>
            <input
              name="swift"
              class="w-full p-2 border rounded"
              bind:value={bankData.swift}
              type="text"
            />
          </div>

          <div>
            <label for="accountNumber" class="block mb-1 font-medium">Account Number</label>
            <input
              name="accountNumber"
              class="w-full p-2 border rounded"
              bind:value={bankData.accountNumber}
              type="text"
            />
          </div>

          <button
            type="submit"
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Submit Invoice
          </button>
        </div>

        <div class="w-[10%]"></div>

        <div class="w-[45%] space-y-4">
          <h3 class="text-xl font-semibold">Add Invoice Item</h3>

          <div>
            <label for="name" class="block mb-1 font-medium">Item Name</label>
            <input
              name="name"
              class="w-full p-2 border rounded"
              type="text"
              bind:value={item.name}
            />
          </div>

          <div>
            <label for="description" class="block mb-1 font-medium">Description</label>
            <input
              name="description"
              class="w-full p-2 border rounded"
              type="text"
              bind:value={item.description}
            />
          </div>

          <div>
            <label for="quantity" class="block mb-1 font-medium">Quantity</label>
            <input
              name="quantity"
              class="w-full p-2 border rounded"
              type="number"
              bind:value={item.quantity}
              min="0"
              step="1"
            />
          </div>

          <div>
            <label for="unitPrice" class="block mb-1 font-medium">Unit Price</label>
            <input
              name="unitPrice"
              class="w-full p-2 border rounded"
              type="number"
              bind:value={item.unitPrice}
              min="0"
              step="0.01"
            />
          </div>

          <button
            type="button"
            class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            onclick={handleAddItem}
          >
            Add Item
          </button>

          
        {#if itemsCount.length>0}
            <div class="mt-4">
              <h4 class="font-semibold mb-2">Items Preview</h4>
              <ul class="space-y-2">
                {#each itemsCount as itm}
                <li class="border p-2 rounded bg-gray-50">
                    <p>
                        <strong>{itm.name}</strong> - {itm.quantity} × ${itm.unitPrice} = {itm.quantity * itm.unitPrice}
                    </p>
                    <p class="text-sm text-gray-600">{itm.description}</p>
                </li>
                {/each}
              </ul>
            </div>
        {/if}
        </div>
      </form>
    </div>
