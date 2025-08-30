<script lang="ts">
  import { browser } from "$app/environment"

  import { page } from '$app/stores';
  import { goto } from "$app/navigation"
  import { deleteInvoiceService, getAllInvoiceService, sendInvoiceEmailService } from "../services/invoice"
  import SideBar from "$lib/components/SideBar.svelte"
  import toast from 'svelte-french-toast';
  import Pagination from "$lib/components/Pagination.svelte"

  let data: any = null
  let loading = true
  let error: string = ""
  let token: string | null = null
  let refresh = 0
  let searchTerm:string=""
  let currentPage: number | null = 1
  let pageSize: number = 10
  let trimmedRows: any[] = []   

  $: currentPage = $page.url.searchParams.get("currentPage")
    ? parseInt($page.url.searchParams.get("currentPage")!)
    : 1
                    
  $: if (refresh >= 0) fetchInvoice()
  $:if(searchTerm) refresh+=1
  $:if(!searchTerm)refresh+=1

  const handleDelete = async (id: string) => {
    try {
      if(!token){
            error="The user has not logged in, Please log in"
            return
        }
      await deleteInvoiceService(id,token)
      toast.success("Receipt Deleted Successfully")
    } catch (err: any) {
      toast.error(err.message)
    }
    refresh += 1
  }

  if (browser) {
    token = localStorage.getItem("token")
  }
  const fetchInvoice = async () => {
    try {
      if(!token){
        error="The user has not logged in, Please log in"
        return
      }
      data = await getAllInvoiceService(token,searchTerm)
      console.log(data)
    } catch (err: any) {
      error = err.message
    } finally {
      loading = false
    }
  }


  const navigateCreate = () => {
    goto("/invoice/create")
  }

  const navigateSign=(id:string)=>{
    goto(`/invoice/signature/${id}`)
  }


  const handleSendEmail=async(invoiceId:string)=>{
    if(!token){
      error="The user has not logged in, Please log in"
      return
    }

    const res=await sendInvoiceEmailService(invoiceId,token)
    toast.success("Email sent successfully")
    
  }
</script>

<SideBar/>
<div class="flex-1 ml-64 p-5">
  {#if loading}
    <p>Loading....</p>
  {:else if error}
    <p class="text-red-500">{error}</p>
  {:else}

      <div>
        <button
          onclick={() => navigateCreate()}
          class="mb-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Create New Invoice
        </button>
        <div class="w-1/3">
          <input
            type="text"
            bind:value={searchTerm}
            class="w-full px-4 py-2 border rounded-md my-2"
            placeholder="Search Invoices"
          />
        </div>
      </div>
      <div class="shadow-md sm:rounded-lg">
        <table
          class="w-full text-sm text-left text-gray-500 dark:text-gray-400"
        >
          <thead
            class="text-xs text-black uppercase bg-gray-50 dark:bg-gray-100 dark:text-black"
          >
            <tr>
              <th class="px-6 py-3">Invoice Number</th>
              <th class="px-6 py-3">Customer Name</th>
              <th class="px-6 py-3">Company Name</th>
              <th class="px-6 py-3">Invoice Date</th>
              <th class="px-6 py-3">Total Amount</th>
              <th class="px-6 py-3">Action</th>
            </tr>
          </thead>
          <tbody>
            {#if trimmedRows.length === 0}
              <tr>
                <td colSpan={6} class="px-6 py-4 text-center">
                  No invoices found.
                </td>
              </tr>
            {:else}
              {#each trimmedRows as invoice}
                <tr
                  class="odd:bg-white even:bg-gray-100 border-b dark:border-gray-700 text-gray-700"
                >
                  <td class="px-6 py-4 font-medium text-black">
                    {invoice.invoiceNumber}
                  </td>
                  <td class="px-6 py-4 capitalize">{invoice.customerName}</td>
                  <td class="px-6 py-4 capitalize">{invoice.companyName}</td>
                  <td class="px-6 py-4">{invoice.invoiceDate}</td>
                  <td class="px-6 py-4"> {invoice.totalAmount} </td>
                  <td class="px-6 py-4 space-x-2">
                    <a
                      href={`http://localhost:3000/invoice/view/${invoice.id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-blue-600 hover:underline"
                    >
                      View
                    </a>
                    <button
                      onclick={() => handleSendEmail(invoice.id)}
                      class="text-green-900 hover:underline"
                    >
                      Email
                    </button>
                    <button
                      class="text-red-500 hover:underline"
                      onclick={() => handleDelete(invoice.id)}
                    >
                      Delete
                    </button>
                    {#if invoice.signatureUrl==null}
                      <button
                      class="text-orange-500 hover:underline"
                      onclick={()=>navigateSign(invoice.id)}
                    >
                      Sign
                    </button>
                    {:else}
                    <button
                      class="text-gray-500"
                    >
                      Signed
                    </button>
                    {/if}
                  </td>
                </tr>
              {/each}
            {/if}
          </tbody>
        </table>
        <Pagination rows={data.items} perPage={pageSize} bind:trimmedRows/>
      </div>
  {/if}
</div>
