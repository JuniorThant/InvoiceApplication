<script>
	
	
    export let rows;
    export let perPage;
	  export let trimmedRows;

    $: totalRows = rows.length 
    $: currentPage = 0
    $: totalPages = Math.ceil(totalRows / perPage) 
    $: start =  currentPage * perPage
    $: end = currentPage === totalPages - 1 ? totalRows - 1 : start + perPage - 1  ;

		$: trimmedRows = rows.slice(start, end + 1);

    $: totalRows, currentPage = 0
    $: currentPage, start, end

</script>

<link rel="stylesheet" href="https://unpkg.com/mono-icons@1.0.5/iconfont/icons.css" >

    {#if totalRows && totalRows > perPage}
        <div class='pagination'>
            <button on:click={() => currentPage -= 1} 
                class="bg-gray-300 p-3 hover:bg-blue-300" 
                disabled={currentPage === 0 ? true : false} 
                aria-label="left arrow icon" 
                aria-describedby="prev">
                   <i class="mi mi-arrow-left"><span class="u-sr-only"></span></i>
            </button>
            <span id='prev' class='sr-only'>Load previous {perPage} rows</span>
            <p>Pages {start + 1} - {end + 1} of {totalRows}</p>
            <button on:click={() => currentPage += 1}
                class="bg-gray-300 p-3 hover:bg-blue-300" 
                disabled={currentPage === totalPages - 1 ? true : false} 
                aria-label="right arrow icon" 
                aria-describedby="next">
                <i class="mi mi-arrow-right"><span class="u-sr-only"></span></i>
            </button>
            <span id='next' class='sr-only'>Load next {perPage} rows</span>
        </div>
    {/if}


<style>
    .sr-only {
      position: absolute;
      clip: rect(1px, 1px, 1px, 1px);
      padding: 0;
      border: 0;
      height: 1px;
      width: 1px;
      overflow: hidden;
    }
    
    .pagination {
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: all;
    }

    .pagination p {
        margin: 0 1rem;
    }
	
	button {
		display: flex;
	}
	
</style>