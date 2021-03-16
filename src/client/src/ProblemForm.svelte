<script lang="ts">
  import { onMount } from 'svelte'
  import { Stretch } from 'svelte-loading-spinners'
  import Collapsible from './Collapsible.svelte'
  import Classification from './Classification.svelte'
  import ReturnedProblem from './ReturnedProblem.svelte'
  import { getProblem } from './api'
  import { persistStateToUrl, loadStateFromUrl } from './urlStore'
  import type { GraphType, Problem } from './types'
  interface FormState {
    activeConstraints: string
    passiveConstraints: string
    leafConstraints?: string
    rootConstraints?: string
    graphType: GraphType
  }

  const FORM_PREFIX = 'problem'

  function formStateToProblem(formState: FormState): Problem {
    return {
      activeConstraints: formState.activeConstraints.split('\n'),
      passiveConstraints: formState.passiveConstraints.split('\n'),
      leafConstraints: formState.leafConstraints?.split('\n'),
      rootConstraints: formState.rootConstraints?.split('\n'),
      isTree: formState.graphType === 'tree',
      isCycle: formState.graphType === 'cycle',
      isPath: formState.graphType === 'path',
    }
  }

  let formState: FormState = {
    activeConstraints: `A B
C C`,
    passiveConstraints: `B B C
A A A
B B B
A A C
B C C`,
    leafConstraints: undefined,
    rootConstraints: undefined,
    graphType: 'tree',
  }

  let response = undefined
  let loading = false
  let showLeafRootConfig = false
  let showExplanation = false
  let openNormalized = false

  onMount(async () => {
    if (window.location.search.includes(`${FORM_PREFIX}_`)) {
      formState = loadStateFromUrl(formState, FORM_PREFIX)
      const problem = formStateToProblem(formState)

      loading = true
      try {
        response = await getProblem(problem, PRODUCTION)
      } catch (e) {
        alert(e.message)
      } finally {
        loading = false
      }
    }
  })

  function handleProblemSubmit(e: any) {
    e.preventDefault()
    persistStateToUrl(formState, FORM_PREFIX)
  }
</script>

<div class="form-wrapper">
  <form>
    <h2>Classify a problem</h2>

    <Collapsible open={showExplanation} label={'Explanation:'}>
      <p>
        The problem specified below, once submitted, will be classified by
        multiple automatic LCL classifiers.
      </p>
      <p>
        The tool uses problem representation similar to <a
          href="https://github.com/olidennis/round-eliminator"
          target="_blank">Round Eliminator</a
        > e.g.
      </p>

      <p>Active configurations:</p>
      <pre>
        {'M U U U\nP P P P'}
      </pre>

      <p>Passive configurations:</p>
      <pre>
        {'M UP UP UP\nU U U U'}
      </pre>

      <p>
        If a problem assumes that the underlying graph is directed (for cycles
        and paths) or rooted (for trees), the directedness is indicated as
        follows:
      </p>

      <p>Active configurations:</p>
      <pre>
        {'M : U U U\nP : P P P'}
      </pre>

      <p>Passive configurations:</p>
      <pre>
        {'M : UP UP UP\nU : U U U'}
      </pre>

      <p>
        Here, the label before the <code>:</code> sign is an output label on the
        incoming edge. So in the example below, we have a rooted tree, in which
        an active node can output <code>M</code> on its incoming edge (and then
        <code>U</code>
        label on all its outgoing edges), or it can output <code>P</code> on its
        incoming edge (and then <code>P</code> label on all its outgoing edges).
      </p>
      <p>
        For more instructions and source code see <a
          href="https://github.com/AleksTeresh/master-thesis"
          target="_blank">this repo on GitHub</a
        >
      </p>
    </Collapsible>

    <label for="activeConfigs">Active configurations:</label>
    <textarea id="activeConfigs" bind:value={formState.activeConstraints} />

    <label for="activeConfigs">Passive configurations:</label>
    <textarea id="passiveConfigs" bind:value={formState.passiveConstraints} />

    <label>
      <input type="radio" bind:group={formState.graphType} value="tree" />
      Tree
    </label>
    <label>
      <input type="radio" bind:group={formState.graphType} value="cycle" />
      Cycle
    </label>
    <label>
      <input type="radio" bind:group={formState.graphType} value="path" />
      Path
    </label>

    <Collapsible open={showLeafRootConfig} label={'Leaf/Root constraints'}>
      <label for="leafConfig">Leaf constraints (optional):</label>
      <textarea id="leafConfig" bind:value={formState.leafConstraints} />

      <label for="rootConfig">Root constraints (optional):</label>
      <textarea id="rootConfig" bind:value={formState.rootConstraints} />
    </Collapsible>
    <button on:click={handleProblemSubmit}> Find </button>
  </form>

  <div>
    {#if loading}
      <Stretch size="60" unit="px" color="#0d0d0d" />
    {/if}
    {#if !loading && response !== undefined}
      <div>
        <h3>Classification:</h3>
        <Classification response={response.result} />
        <Collapsible open={openNormalized} label={'Normalized representation:'}>
          <ReturnedProblem item={response.problem} />
        </Collapsible>
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

  pre {
    padding-left: 10px;
  }
</style>
