<script lang="ts">
  import { Complexity } from '../types'
  import type { Source } from '../types'

  export let source: Source
  export let lowerBound: Complexity | undefined = undefined
  export let upperBound: Complexity | undefined = undefined
</script>

{#if source && lowerBound != Complexity.Const && upperBound != Complexity.Unsolvable}
  (by
  <a target="_blank" href={source.urls[0]}>{source.name} </a>)
{/if}
