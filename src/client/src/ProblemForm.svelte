<script lang="ts">
  import { onMount } from 'svelte'
  import { Stretch } from 'svelte-loading-spinners'
  import Collapsible from './Collapsible.svelte'
  import Classification from './Classification.svelte'
	import { getProblem } from './api'
  import type { GraphType, Problem } from './types'

	let activeConstraints = `A B
    C C`
	let passiveConstraints = `B B C
    A A A
    B B B
    A A C
    B C C`
	let leafConstraints = undefined
	let rootConstraints = undefined

	let graphType: 'tree' | 'cycle' | 'path' = 'path'
  let response = undefined
  let loading = false

  let showLeafRootConfig = false

  onMount(async () => {
    if (!!window.location.search) {
      const params = new URLSearchParams(location.search)
      activeConstraints = params.get('problem_activeConstraints')
      passiveConstraints = params.get('problem_passiveConstraints')
      leafConstraints = params.get('problem_leafConstraints')
      rootConstraints = params.get('problem_rootConstraints')
      graphType = params.get('problem_graphType') as GraphType

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
        console.log(response)
      } catch (e) {
        alert('Error')
      } finally {
        loading = false
      }
    }
  })

	function handleProblemSubmit(e: any) {
		e.preventDefault()
    const params = new URLSearchParams(location.search)
    params.set('problem_activeConstraints', activeConstraints)
    params.set('problem_passiveConstraints', passiveConstraints)
    if (leafConstraints)
      params.set('problem_leafConstraints', leafConstraints)
    if (rootConstraints)
      params.set('problem_rootConstraints', rootConstraints)
    params.set('problem_graphType', graphType)
    window.location.search = params.toString()
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
  
    <Collapsible
      open={showLeafRootConfig}
      label={"Leaf/Root constraints"}>
      <label for="leafConfig">Leaf constraints (optional):</label>
      <textarea id="leafConfig" bind:value={leafConstraints}></textarea>
  
      <label for="rootConfig">Root constraints (optional):</label>
      <textarea id="rootConfig" bind:value={rootConstraints}></textarea>
    </Collapsible>
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
        <Classification
          response={response} />
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

  textarea {
    width: 250px;
    height: 100px;
  }
</style>
