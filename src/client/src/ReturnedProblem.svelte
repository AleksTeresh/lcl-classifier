<script>
  import { getGraphType } from './graph'

  export let item
</script>

<p>Active config:</p>
{#each item.activeConstraints as c}
  <div>{c}</div>
{/each}
<p>Passive config:</p>
{#each item.passiveConstraints as c}
  <div>{c}</div>
{/each}
<p>Graph: {getGraphType(item)}</p>
{#if item.rootConstraints.length !== 0}
  <p>Root config: {item.rootConstraints}</p>
{/if}
{#if item.leafConstraints.length !== 0}
  <p>Leaf config: {item.leafConstraints}</p>
{/if}

<style>
  p {
    margin-bottom: 5px;
  }
</style>
