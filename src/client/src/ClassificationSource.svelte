<script>
  export let source
</script>

{#if source}
  (by
  <a
    target="_blank"
    href={source.urls[0]}>{source.name}
  </a>)
{/if}
