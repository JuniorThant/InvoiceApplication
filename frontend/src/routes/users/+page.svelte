<script lang="ts">
  import { browser } from "$app/environment"

  import { onMount } from "svelte"
  import SideBar from "$lib/components/SideBar.svelte"
  import toast from "svelte-french-toast"
  import { page } from '$app/stores';
  import {
    changeRoleService,
    deleteUserService,
    getUsersService,
  } from "../services/auth"
  import { goto } from "$app/navigation"
  import Pagination from "$lib/components/Pagination.svelte"

  let data: any = null
  let loading = true
  let error: string = ""
  let token: string | null = null
  let searchTerm: string = ""
  let deleteModal: boolean = false
  let deleteInput: string = ""
  let userValue: string = ""
  let deleteMessage: string = ""
  let pageSize: number = 10
  let trimmedRows: any[] = []
  let refresh:number=0
  
  $: if (refresh >= 0) fetchUsers()
  $:if(searchTerm) refresh+=1
  $:if(!searchTerm)refresh+=1

  $: currentPage = $page.url.searchParams.get("currentPage")
    ? parseInt($page.url.searchParams.get("currentPage")!)
    : 1

  if (browser) {
    token = localStorage.getItem("token")
  }
  const fetchUsers = async () => {
    try {
      if (!token) {
        error = "The user has not logged in, Please log in"
        return
      }
      const res = await getUsersService(token,searchTerm)
      data = { ...res.data }
    } catch (err: any) {
      error = err.message
    } finally {
      loading = false
    }
  }

  onMount(() => {
    fetchUsers()
  })

  const handleRole = async (userId: string) => {
    if (!token) {
      error = "The user has not logged in, Please log in"
      return
    }
    const res = await changeRoleService(token, userId)
    console.log(res)
    if (res) {
      toast.success("The user role updated suceessfully")
    }
    fetchUsers()
  }

  const handleDelete = (userId: string) => {
    deleteModal = true
    userValue = userId
  }

  const handleCancel = () => {
    deleteModal = false
  }

  const navigateCreate = () => {
    goto("/users/register")
  }

  const handleConfirm = async () => {
    deleteMessage = ""
    if (userValue == "") {
      toast.error("Invalid User ID")
      return
    }
    if (!token) {
      error = "The user has not logged in, Please log in"
      return
    }
    if (deleteInput == "DELETE") {
      await deleteUserService(userValue, token)
      toast.success("User deleted successfully")
      deleteModal=false
      fetchUsers()
    } else {
      deleteMessage = "Please type DELETE"
    }
  }
</script>

<SideBar />
<div class="flex-1 ml-64 p-5">
  {#if loading}
    <p>Loading....</p>
  {:else if error}
    <p class="text-red-500">{error}</p>
  {:else}
    {#if deleteModal == true}
      <div class="rounded-md shadow-lg top-[40%] left-[40%] absolute p-5 z-10">
        <p>Do you want to delete user?</p>
        <p>Type "DELETE" to delete this user</p>
        {#if deleteMessage}
          <p class="text-red-500 mt-3">{deleteMessage}</p>
        {/if}
        <input
          type="text"
          bind:value={deleteInput}
          placeholder="DELETE"
          class="px-4 py-2 border rounded-md my-2"
        />
        <div class="justify-end flex">
          <button
            on:click={handleCancel}
            class="bg-green-600 text-white rounded-md p-2 m-1 hover:bg-green-400"
            >Cancel</button
          >
          <button
            class="bg-red-600 text-white rounded-md p-2 m-1 hover:bg-red-400"
            on:click={handleConfirm}>Confirm</button
          >
        </div>
      </div>
    {/if}

    <div>
      <button
          on:click={navigateCreate}
          class="mb-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Register New User
        </button>
      <div class="w-1/3">
        <input
          type="text"
          bind:value={searchTerm}
          class="w-full px-4 py-2 border rounded-md my-2"
          placeholder="Search Users"
        />
      </div>
    </div>
    <div class="shadow-md sm:rounded-lg">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead
          class="text-xs text-black uppercase bg-gray-50 dark:bg-gray-100 dark:text-black"
        >
          <tr>
            <th class="px-6 py-3">Name</th>
            <th class="px-6 py-3">Email</th>
            <th class="px-6 py-3">Role</th>
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
            {#each trimmedRows as user}
              <tr
                class="odd:bg-white even:bg-gray-100 border-b dark:border-gray-700 text-gray-700"
              >
                <td class="px-6 py-4 font-medium text-black">
                  {user.name}
                </td>
                <td class="px-6 py-4">{user.email}</td>
                <td class="px-6 py-4 capitalize">
                  {#if user.isSuperuser == true}
                    Admin
                  {:else}
                    User
                  {/if}
                </td>
                <td class="px-6 py-4 space-x-2">
                  <button
                    class="text-green-500 hover:underline"
                    on:click={() => handleRole(user.id)}
                  >
                    Change Role
                  </button>
                  <button
                    class="text-red-500 hover:underline"
                    on:click={() => handleDelete(user.id)}
                  >
                    Delete User
                  </button>
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
