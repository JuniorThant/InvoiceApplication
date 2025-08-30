<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import "../../app.css";
	let { children } = $props();
	import {Toaster} from 'svelte-french-toast';

</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex">
	<Toaster/>
	{@render children?.()}
</div>
