<script lang="ts">
  import { onMount } from "svelte"
  import { Stretch } from "svelte-loading-spinners"
  import Collapsible from "./Collapsible.svelte"
  import Classification from "./Classification.svelte"
  import { getProblem } from "./api"
  import { persistStateToUrl, loadStateFromUrl } from "./urlStore"
  import type { GraphType, Problem } from "./types"
  interface FormState {
    activeConstraints: string
    passiveConstraints: string
    leafConstraints?: string
    rootConstraints?: string
    graphType: GraphType
  }

  const FORM_PREFIX = "problem"

  function formStateToProblem(formState: FormState): Problem {
    return {
      activeConstraints: formState.activeConstraints.split("\n"),
      passiveConstraints: formState.passiveConstraints.split("\n"),
      leafConstraints: formState.leafConstraints?.split("\n"),
      rootConstraints: formState.rootConstraints?.split("\n"),
      isTree: formState.graphType === "tree",
      isCycle: formState.graphType === "cycle",
      isPath: formState.graphType === "path",
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
    graphType: "path",
  }

  let response = undefined
  let loading = false
  let showLeafRootConfig = false

  onMount(async () => {
    if (window.location.search.includes(`${FORM_PREFIX}_`)) {
      formState = loadStateFromUrl(formState, FORM_PREFIX)
      const problem = formStateToProblem(formState)

      loading = true
      try {
        response = await getProblem(problem, PRODUCTION)
        console.log(response)
      } catch (e) {
        alert("Error")
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
    <h2>Find a problem</h2>
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

    <Collapsible open={showLeafRootConfig} label={"Leaf/Root constraints"}>
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
        <Classification {response} />
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
