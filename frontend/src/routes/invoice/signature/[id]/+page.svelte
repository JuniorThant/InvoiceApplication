<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import toast from 'svelte-french-toast';
  import { goto } from '$app/navigation'

  let token: string | null = null;
  let id: string | undefined = "";

  if (browser) {
    token = localStorage.getItem("token");
  }

  $: id = $page.params.id;

  let file: File | null = null;

  const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      file = target.files[0];
    }
  };

  const handleSubmit = async (event: Event) => {
    event.preventDefault();

    if (!token) {
      toast.error("The user has not logged in, Please log in");
      return;
    }

    if (!id) {
      toast.error("No invoice ID found");
      return;
    }

    if (!file) {
      toast.error("Please select a signature image");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file); 

      const res = await fetch(`http://localhost:8015/invoice/${id}/signature`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!res.ok) {
        throw new Error(await res.text());
      }

      toast.success("Signature uploaded successfully!");
      goto("/invoice")
    } catch (error) {
      console.error(error);
      toast.error("Failed to upload signature");
    }
  };
</script>

<div class="flex justify-center items-center min-h-[50vh] bg-gray-50 w-full">
  <form
    class="flex flex-col gap-4 p-6 bg-white shadow-md rounded-2xl w-full max-w-md"
    on:submit|preventDefault={handleSubmit}
  >
    <h2 class="text-xl font-semibold text-gray-800 text-center">Upload Signature</h2>

    <input
      class="border border-gray-300 rounded-lg px-3 py-2 text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
      type="file"
      accept="image/*"
      on:change={handleFileChange}
    />

    <button
      type="submit"
      class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition-colors font-medium shadow-sm"
    >
      Upload
    </button>
  </form>
</div>

