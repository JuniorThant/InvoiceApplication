<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte'

  let username = '';
  let password = '';
  let error = '';

  async function handleLogin(event: Event) {
    event.preventDefault()
    try{
        const res=await fetch("http://localhost:8015/api/access/login",{
            method:'POST',
            headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
            },
            body:new URLSearchParams({
                username,
                password
            })
        })

        if(!res.ok){
            throw new Error("Invalid Username or Password")
        }
        if(res.status===403){
            throw new Error("Invalid Username or Password")
        }

        const data=await res.json()
        localStorage.setItem("token",data.access_token)
        document.cookie = `token=${data.access_token}; path=/; max-age=${60 * 60 * 24}; secure`;
        
        goto("/invoice")
    }catch(e:any){
        console.log("Error Message: ",e.message)
        error=e.message
    }
  }

</script>

<div class="flex flex-col items-center justify-center h-screen">
  <form on:submit|preventDefault={handleLogin} class="bg-white p-6 rounded shadow-md w-80 space-y-4">
    <h2 class="text-xl font-bold text-center">Login</h2>

    {#if error}
      <p class="text-red-500 text-sm">{error}</p>
    {/if}

    <input
      type="text"
      placeholder="Username"
      bind:value={username}
      class="border p-2 w-full rounded"
      required
    />

    <input
      type="password"
      placeholder="Password"
      bind:value={password}
      class="border p-2 w-full rounded"
      required
    />

    <button
      type="submit"
      class="bg-blue-500 text-white px-4 py-2 w-full rounded hover:bg-blue-600"
    >
      Login
    </button>
  </form>
</div>
