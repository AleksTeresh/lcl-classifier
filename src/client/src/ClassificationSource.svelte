<script>
  import { Complexity } from './types'

  export let source
  export let lowerBound
  export let upperBound
</script>

{#if source && lowerBound != Complexity.Const && upperBound != Complexity.Unsolvable}
  (by
  <a target="_blank" href={source.urls[0]}>{source.name} </a>)
{/if}
