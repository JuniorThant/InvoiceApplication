<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import toast from 'svelte-french-toast';

  let token: string | null = null;
  let invoiceHtml: string = "";
  let id: string|undefined = "";

  if (browser) {
    token = localStorage.getItem("token");
  }

  $: id = $page.params.id;

  const fetchInvoiceTemplate = async () => {
    if (!token) {
      toast.error("The user has not logged in, Please log in");
      return;
    }

    if (!id) return; 

    try {
      const res = await fetch(`http://localhost:8015/invoice/${id}/preview`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      invoiceHtml = await res.text();
    } catch (error) {
      toast.error("Failed to fetch invoice");
      console.error(error);
    }
  };

  onMount(() => {
    fetchInvoiceTemplate();
  });
</script>


<div class="invoice-container">
  <div class="invoice-scale">
    {@html invoiceHtml}
  </div>
</div>

<style>

  .invoice-container {
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 2rem;
    background: #f8f9fa; 
  }


  .invoice-scale {
    transform: scale(1.2); 
    transform-origin: top center;
    background: white;
    padding: 2rem;
    box-shadow: 0 0 10px rgba(0,0,0,0.15);
  }


</style>






