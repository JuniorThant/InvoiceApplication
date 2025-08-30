<script lang="ts">
  import { browser } from '$app/environment'
  import { goto } from '$app/navigation';
  import toast from 'svelte-french-toast'
  import { createUserService } from '../../services/auth'
  import SideBar from '$lib/components/SideBar.svelte'

  let formData:any={
    name:"",
    email:"",
    password:""
  }
  let error:string|null=null
  let token:string|null=null
  if (browser){
    token=localStorage.getItem("token")
  }

  async function handleRegister(event: Event) {
    event.preventDefault()

    if(!token){
        error="The user has not logged in, Please log in"
        return
    }
    try{
        const res=await createUserService(formData,token)
        if(res){
            toast.success("The user created successfully")
        }
        goto("/users")
    }catch(e:any){
        console.log("Error Message: ",e.message)
        error=e.message
    }
  }


</script>

<SideBar/>
<div class="flex-1 ml-64 p-5">
  <div class="flex flex-col items-center justify-center h-screen">
    <form on:submit|preventDefault={handleRegister} class="bg-white p-6 rounded shadow-md w-80 space-y-4">
      <h2 class="text-xl font-bold text-center">Register</h2>

      {#if error}
        <p class="text-red-500 text-sm">{error}</p>
      {/if}

      <input
        type="text"
        placeholder="Name"
        bind:value={formData.name}
        class="border p-2 w-full rounded"
        required
      />

      <input
        type="email"
        placeholder="Email"
        bind:value={formData.email}
        class="border p-2 w-full rounded"
        required
      />

      <input
        type="password"
        placeholder="Password"
        bind:value={formData.password}
        class="border p-2 w-full rounded"
        required
      />

      <button
        type="submit"
        class="bg-blue-500 text-white px-4 py-2 w-full rounded hover:bg-blue-600"
      >
        Register
      </button>
    </form>
  </div>
</div>