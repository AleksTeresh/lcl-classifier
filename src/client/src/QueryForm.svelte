<script lang="ts">
  import { Stretch } from 'svelte-loading-spinners'
  import { getQueryResult } from './api'
	import type { Query } from './types'
  import { Complexity } from './types'

  function getGraphType(problem: any) {
    if (problem.isTree) {
      return 'Tree'
    }
    if (problem.isCycle) {
      return 'Cycle'
    }
    if (problem.isPath) {
      return 'Path'
    }
  }

	let graphType: 'tree' | 'cycle' | 'path' = 'path'
	let isDirectedOrRooted: boolean = false
	let isRegular: boolean = true

  let randLowerBound = Complexity.IteratedLog
  let randUpperBound = Complexity.LogLog
  let detLowerBound = Complexity.Const
  let detUpperBound = Complexity.Unsolvable

  let activeDegree = 2
  let passiveDegree = 2
  let labelCount = 3
  let activesAllSame = false
  let passivesAllSame = false

  let largestProblemOnly = false
  let smallestProblemOnly = false
  let excludeIfConfigHasAllOf = ""
  let excludeIfConfigHasSomeOf = ""
  let includeIfConfigHasAllOf = ""
  let includeIfConfigHasSomeOf = ""

  let loading = false
  let response = undefined

	async function handleProblemSubmit(e: any) {
		e.preventDefault();

		const query: Query = {
			isTree: graphType === 'tree',
			isCycle: graphType === 'cycle',
			isPath: graphType === 'path',
			isDirectedOrRooted,
			isRegular,

      randLowerBound,
      randUpperBound,
      detLowerBound,
      detUpperBound,
      
      activeDegree,
      passiveDegree,
      labelCount,
      activesAllSame,
      passivesAllSame,

      largestProblemOnly,
      smallestProblemOnly,
      excludeIfConfigHasAllOf: excludeIfConfigHasAllOf.split('\n'),
      excludeIfConfigHasSomeOf: excludeIfConfigHasSomeOf.split('\n'),
      includeIfConfigHasAllOf: includeIfConfigHasAllOf.split('\n'),
      includeIfConfigHasSomeOf: includeIfConfigHasSomeOf.split('\n')
		}

    loading = true
    try {
      response = await getQueryResult(query, PRODUCTION)
    } catch (e) {
      alert('Error')
    } finally {
      loading = false
    }
	}
</script>

<div class="form-wrapper">
  <form>
    <h2>Execute a query</h2>
    <h4>Problem class</h4>
    <label for="active-degree">Active degree:</label>
    <input id="active-degree" type="number" min=1 max=100 bind:value={activeDegree} />
  
    <label for="passive-degree">Passive degree:</label>
    <input id="passive-degree" type="number" min=1 max=100 bind:value={passiveDegree} />
  
    <label for="label-count">Label count:</label>
    <input id="label-count" type="number" min=1 max=100 bind:value={labelCount} />
  
    <label>
      <input type=checkbox bind:checked={activesAllSame}>
      Active configs are all the same
    </label>
  
    <label>
      <input type=checkbox bind:checked={passivesAllSame}>
      Passive configs are all the same
    </label>
  
    <h4>Graph properties</h4>
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
  
    <label>
      <input type=checkbox bind:checked={isDirectedOrRooted}>
      Directed or rooted
    </label>
    <label>
      <input type=checkbox bind:checked={isRegular}>
      Regular
    </label>
  
    <div>
      <div class="inline-radio-wrapper">
        <h4>Random lower bound</h4>
        {#each Object.entries(Complexity) as [_, value]}
          <label class="inline-radio">
            <input type=radio bind:group={randLowerBound} value={value}>
            {value}
          </label>
        {/each}
      </div>
      <div class="inline-radio-wrapper">
        <h4>Random upper bound</h4>
        {#each Object.entries(Complexity) as [_, value]}
          <label class="inline-radio">
            <input type=radio bind:group={randUpperBound} value={value}>
            {value}
          </label>
        {/each}
      </div>
      <div class="inline-radio-wrapper">
        <h4>Deterministic lower bound</h4>
        {#each Object.entries(Complexity) as [_, value]}
          <label class="inline-radio">
            <input type=radio bind:group={detLowerBound} value={value}>
            {value}
          </label>
        {/each}
      </div>
      <div class="inline-radio-wrapper">
        <h4>Deterministic upper bound</h4>
        {#each Object.entries(Complexity) as [_, value]}
          <label class="inline-radio">
            <input type=radio bind:group={detUpperBound} value={value}>
            {value}
          </label>
        {/each}
      </div>
    </div>
  
    <h4>Filter the problems:</h4>
    <div>
      <label>
        <input type=checkbox bind:checked={largestProblemOnly}>
        Return largest problem only
      </label>
    
      <label>
        <input type=checkbox bind:checked={smallestProblemOnly}>
        Return smallest problem only
      </label>
    
      <label for="exclude-if-all">Exclude if configs have <strong>all</strong> of</label>
      <textarea id="exclude-if-all" bind:value={excludeIfConfigHasAllOf}></textarea>
    
      <label for="exclude-if-some">Exclude if configs have <strong>some</strong> of</label>
      <textarea id="exclude-if-some" bind:value={excludeIfConfigHasSomeOf}></textarea>
    
      <label for="include-if-all">Include if configs have <strong>all</strong> of</label>
      <textarea id="include-if-all" bind:value={includeIfConfigHasAllOf}></textarea>
    
      <label for="include-if-some">Include if configs have <strong>some</strong> of</label>
      <textarea id="include-if-some" bind:value={includeIfConfigHasSomeOf}></textarea>
    </div>
  
    <button
      on:click={handleProblemSubmit}>
      Search
    </button>
  </form>

  <div>
    {#if loading}
      <Stretch size="60" unit="px" color="#0d0d0d"></Stretch>
    {/if}
    {#if !loading && response !== undefined}
      <p>Total # of problems: {response.length}</p>
      {#each response as prob}
        <div class="problem-wrapper">
          <h5>Problem:</h5>
          <p>Active config: {prob.activeConstraints}</p>
          <p>Passive config: {prob.passiveConstraints}</p>
          <p>Graph: {getGraphType(prob)}</p>
          {#if prob.rootConstraints.length !== 0}
            <p>Root config: {prob.rootConstraints}</p>
          {/if}
          {#if prob.leafConstraints.length !== 0}
            <p>Leaf config: {prob.leafConstraints}</p>
          {/if}
          <h5>Classification:</h5>
          <p>Det. lower bound: {prob.detLowerBound}</p>
          <p>Det. upper bound: {prob.detUpperBound}</p>
          <p>Rand. lower bound: {prob.randLowerBound}</p>
          <p>Rand. upper bound: {prob.randUpperBound}</p>
        </div>
      {/each}
    {/if}
  </div>
</div>

<style>
	.form-wrapper {
		margin: 20px;
	}

  .inline-radio {
    display: inline;
    margin-right: 15px;
  }

  .inline-radio-wrapper {
    margin-bottom: 15px;
  }

  .problem-wrapper {
    border-bottom: 1px solid black;
  }

  textarea {
    width: 250px;
    height: 100px;
  }
</style>
