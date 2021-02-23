<script lang="ts">
  import { Stretch } from 'svelte-loading-spinners'
	import { getProblem } from './api'
	import type { Problem } from './types';

	let activeConstraints = `
    A B
    C C`
	let passiveConstraints = `
    B B C
    A A A
    B B B
    A A C
    B C C`
	let leafConstraints = undefined
	let rootConstraints = undefined

	let graphType: 'tree' | 'cycle' | 'path' = 'path'
  let response = undefined
  let loading = false

	async function handleProblemSubmit(e: any) {
		e.preventDefault()

		const problem: Problem = {
			activeConstraints: activeConstraints.split('\n'),
			passiveConstraints: passiveConstraints.split('\n'),
			leafConstraints: leafConstraints?.split('\n'),
			rootConstraints: rootConstraints?.split('\n'),
			isTree: graphType === 'tree',
			isCycle: graphType === 'cycle',
			isPath: graphType === 'path',
		}
    loading = true
    try {
      response = await getProblem(problem, PRODUCTION)
    } catch (e) {
      alert('Error')
    } finally {
      loading = false
    }
	}
</script>

<div class="form-wrapper">
  <form>
    <h2>Find a problem</h2>
    <label for="activeConfigs">Active configurations:</label>
    <textarea id="activeConfigs" bind:value={activeConstraints}></textarea>
  
    <label for="activeConfigs">Passive configurations:</label>
    <textarea id="passiveConfigs" bind:value={passiveConstraints}></textarea>
  
    <label>
      <input type=radio bind:group={graphType} value="tree">
      Tree
    </label>
    <label>
      <input type=radio bind:group={graphType} value="cycle">
      Cycle
    </label>
    <label>
      <input type=radio bind:group={graphType} value="path">
      Path
    </label>
  
    {#if graphType === 'path'}
      <label for="leafConfig">Leaf constraints (optional):</label>
      <textarea id="leafConfig" bind:value={leafConstraints}></textarea>
  
      <label for="rootConfig">Root constraints (optional):</label>
      <textarea id="rootConfig" bind:value={rootConstraints}></textarea>
    {/if}
  
    <button
      on:click={handleProblemSubmit}>
      Find
    </button>
  </form>
  
  <div>
    {#if loading}
      <Stretch size="60" unit="px" color="#0d0d0d"></Stretch>
    {/if}
    {#if !loading && response !== undefined}
      <div>
        <h3>Classification:</h3>
        <p>Det. lower bound: {response.detLowerBound}</p>
        <p>Det. upper bound: {response.detUpperBound}</p>
        <p>Rand. lower bound: {response.randLowerBound}</p>
        <p>Rand. upper bound: {response.randUpperBound}</p>
      </div>
    {/if}
  </div>
</div>

<style>
	.form-wrapper {
		margin: 20px;
	}

  button {
    display: block;
  }
</style>
