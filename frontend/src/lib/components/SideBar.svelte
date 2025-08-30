<script lang="ts">
  import { onMount } from "svelte"
  import { getMeService } from "../../routes/services/auth"
  import { browser } from "$app/environment"
  import toast from "svelte-french-toast"

  let token:string|null=null
  let isSuperuser:boolean=false
  if(browser){
    token=localStorage.getItem("token")
  }
    const isActive=(path:string)=>{
        return typeof window !== "undefined" && window.location.pathname.startsWith(path);
    }

    onMount(()=>{
      const fetchUser=async()=>{
        if(!token){
          toast.error("The user has not logged in, Please log in")
          return
        }
        const res=await getMeService(token)
        if(res.isSuperuser){
          isSuperuser=res.isSuperuser
          console.log(isSuperuser)
        }
      }
      fetchUser()
    })
</script>

<div class="w-64 h-screen bg-gray-100 text-gray-800 p-4 border-r fixed top-0 left-0 z-40 overflow-y-auto">
  <h2 class="text-2xl font-bold mb-8 text-gray-900">Invoice System</h2>
  <nav>
    <ul>
      <li>
        <a
          href="/invoice"
          class="block py-2 px-4 rounded {isActive('/invoice') ? 'bg-gray-400' : 'hover:bg-gray-200'}"
        >
          Invoices
        </a>
      </li>
      <li>
        <a
          href="/receipt"
          class="block py-2 px-4 rounded {isActive('/receipt') ? 'bg-gray-400' : 'hover:bg-gray-200'}"
        >
          Receipts
        </a>
      </li>
      {#if isSuperuser==true}
      <li>
        <a
          href="/users"
          class="block py-2 px-4 rounded {isActive('/users') ? 'bg-gray-400' : 'hover:bg-gray-200'}"
        >
          Users
        </a>
      </li>
      {/if}

    </ul>
  </nav>
</div>