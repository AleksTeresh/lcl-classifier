<script lang="ts">
  import './response.css'
  import { onMount } from 'svelte'
  import { Stretch } from 'svelte-loading-spinners'
  import VirtualList from '@sveltejs/svelte-virtual-list'
  import Statistics from './Statistics.svelte'
  import { readyQueries } from './readyQueries'
  import Classification from './Classification.svelte'
  import Collapsible from './Collapsible.svelte'
  import { getQueryResult, getTotalProblemCount } from './api'
  import { persistStateToUrl, loadStateFromUrl } from './urlStore'
  import type {
    Query,
    ClassifiedProblem,
    QueryStatistics,
    GraphType,
  } from './types'
  import { Complexity } from './types'

  interface QueryResponse {
    problems: ClassifiedProblem[]
    stats: QueryStatistics
    isComplete: boolean
  }

  interface FormState {
    graphType: GraphType
    isDirectedOrRooted: boolean

    randLowerBound: Complexity
    randUpperBound: Complexity
    detLowerBound: Complexity
    detUpperBound: Complexity

    activeDegree: number
    passiveDegree: number
    labelCount: number
    activesAllSame: boolean
    passivesAllSame: boolean

    largestProblemOnly: boolean
    smallestProblemOnly: boolean
    completelyRandUnclassifiedOnly: boolean
    partiallyRandUnclassifiedOnly: boolean
    completelyDetUnclassifiedOnly: boolean
    partiallyDetUnclassifiedOnly: boolean
    excludeIfConfigHasAllOf: string
    excludeIfConfigHasSomeOf: string
    includeIfConfigHasAllOf: string
    includeIfConfigHasSomeOf: string
  }

  interface ExtraConfigs {
    fetchStatsOnly: boolean
  }

  const FORM_PREFIX = 'query'

  function formStateToQuery(
    formState: FormState,
    extraConfigs: ExtraConfigs
  ): Query {
    return {
      ...formState,
      ...extraConfigs,
      isTree: formState.graphType === 'tree',
      isCycle: formState.graphType === 'cycle',
      isPath: formState.graphType === 'path',
      excludeIfConfigHasAllOf: formState.excludeIfConfigHasAllOf.split('\n'),
      excludeIfConfigHasSomeOf: formState.excludeIfConfigHasSomeOf.split('\n'),
      includeIfConfigHasAllOf: formState.includeIfConfigHasAllOf.split('\n'),
      includeIfConfigHasSomeOf: formState.includeIfConfigHasSomeOf.split('\n'),
    }
  }

  function getGraphType(problem: ClassifiedProblem) {
    if (problem.flags.isTree) {
      return 'Tree'
    }
    if (problem.flags.isCycle) {
      return 'Cycle'
    }
    if (problem.flags.isPath) {
      return 'Path'
    }
  }

  let formState: FormState = {
    graphType: 'path',
    isDirectedOrRooted: false,

    randLowerBound: Complexity.Const,
    randUpperBound: Complexity.Unsolvable,
    detLowerBound: Complexity.Const,
    detUpperBound: Complexity.Unsolvable,

    activeDegree: 2,
    passiveDegree: 2,
    labelCount: 3,
    activesAllSame: false,
    passivesAllSame: false,

    largestProblemOnly: false,
    smallestProblemOnly: false,
    completelyRandUnclassifiedOnly: false,
    partiallyRandUnclassifiedOnly: false,
    completelyDetUnclassifiedOnly: false,
    partiallyDetUnclassifiedOnly: false,
    excludeIfConfigHasAllOf: '',
    excludeIfConfigHasSomeOf: '',
    includeIfConfigHasAllOf: '',
    includeIfConfigHasSomeOf: '',
  }

  let loading = false
  let response: QueryResponse = undefined
  let problemCount = ''

  let showExcludeInclude = false
  let showComplexity = false
  let showStatistics = false
  let showProblems = false
  let showPremadeQueries = false
  let showExplanation = false

  onMount(async () => {
    try {
      const r = await getTotalProblemCount(PRODUCTION)
      problemCount = r.problemCount
    } catch (e) {
      alert(e.message)
    } finally {
      loading = false
    }
    if (window.location.search.includes(`${FORM_PREFIX}_`)) {
      let augmentedFormState = {
        ...formState,
        fetchStatsOnly: true,
      }
      augmentedFormState = loadStateFromUrl(augmentedFormState, FORM_PREFIX)

      formState = augmentedFormState
      const { fetchStatsOnly } = augmentedFormState
      const query = formStateToQuery(formState, { fetchStatsOnly })

      loading = true
      try {
        response = await getQueryResult(query, PRODUCTION)
      } catch (e) {
        alert(e.message)
      } finally {
        loading = false
      }
    }
  })

  async function handleQuerySubmission(fetchStatsOnly: boolean) {
    persistStateToUrl(
      {
        ...formState,
        fetchStatsOnly,
      },
      FORM_PREFIX
    )
  }

  async function fetchStatsAndProblems(e: any) {
    e.preventDefault()
    handleQuerySubmission(false)
  }

  async function fetchStatsOnly(e: any) {
    e.preventDefault()
    handleQuerySubmission(true)
  }
</script>

<div class="form-wrapper">
  <form>
    <h2>Search among classified problems</h2>

    <p>
      Total number of problems in the database: {problemCount}<br />
      All of the data is also available at
      <a href="https://zenodo.org/record/4587681">Zenodo</a>
    </p>

    <Collapsible open={showExplanation} label={'Explanation:'}>
      <p>
        The form below allows to query our database containing {problemCount}
        preclassifed problems. Alongside the problems satisfying
        the query, some statistics about the problems will be returned as well.
      </p>
    </Collapsible>

    <Collapsible open={showPremadeQueries} label={'Here are some examples of interesting queries:'}>
      <ul>
        {#each readyQueries as q}
          <li><a href={q.href}>{q.linkText}</a>{q.afterText}</li>
        {/each}
      </ul>
    </Collapsible>

    <h4>Problem class</h4>
    <label for="active-degree">Active degree:</label>
    <input
      id="active-degree"
      type="number"
      min="1"
      max="100"
      bind:value={formState.activeDegree}
    />

    <label for="passive-degree">Passive degree:</label>
    <input
      id="passive-degree"
      type="number"
      min="1"
      max="100"
      bind:value={formState.passiveDegree}
    />

    <label for="label-count">Label count:</label>
    <input
      id="label-count"
      type="number"
      min="1"
      max="100"
      bind:value={formState.labelCount}
    />

    <h4>Graph properties</h4>
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

    <label>
      <input type="checkbox" bind:checked={formState.isDirectedOrRooted} />
      Directed or rooted
    </label>

    <Collapsible open={showComplexity} label={'Complexity:'}>
      <div class="inline-radio-wrapper">
        <label>
          <input
            type="checkbox"
            bind:checked={formState.completelyRandUnclassifiedOnly}
          />
          Only completely unclassified (in rand. setting)
        </label>
        <label>
          <input
            type="checkbox"
            bind:checked={formState.partiallyRandUnclassifiedOnly}
          />
          Only partially unclassified (in rand. setting)
        </label>
        <label>
          <input
            type="checkbox"
            bind:checked={formState.completelyDetUnclassifiedOnly}
          />
          Only completely unclassified (in det. setting)
        </label>
        <label>
          <input
            type="checkbox"
            bind:checked={formState.partiallyDetUnclassifiedOnly}
          />
          Only partially unclassified (in det. setting)
        </label>

        <p class="boldenned">Random lower bound</p>
        {#each Object.entries(Complexity) as [_, value]}
          <label class="inline-radio">
            <input type="radio" bind:group={formState.randLowerBound} {value} />
            {value}
          </label>
        {/each}
      </div>
      <div class="inline-radio-wrapper">
        <p class="boldenned">Random upper bound</p>
        {#each Object.entries(Complexity) as [_, value]}
          <label class="inline-radio">
            <input type="radio" bind:group={formState.randUpperBound} {value} />
            {value}
          </label>
        {/each}
      </div>
      <div class="inline-radio-wrapper">
        <p class="boldenned">Deterministic lower bound</p>
        {#each Object.entries(Complexity) as [_, value]}
          <label class="inline-radio">
            <input type="radio" bind:group={formState.detLowerBound} {value} />
            {value}
          </label>
        {/each}
      </div>
      <div class="inline-radio-wrapper">
        <p class="boldenned">Deterministic upper bound</p>
        {#each Object.entries(Complexity) as [_, value]}
          <label class="inline-radio">
            <input type="radio" bind:group={formState.detUpperBound} {value} />
            {value}
          </label>
        {/each}
      </div>
    </Collapsible>

    <Collapsible open={showExcludeInclude} label={'Configs restrictions:'}>
      <label>
        <input type="checkbox" bind:checked={formState.activesAllSame} />
        Active configs are all the same
      </label>

      <label>
        <input type="checkbox" bind:checked={formState.passivesAllSame} />
        Passive configs are all the same
      </label>

      <label>
        <input type="checkbox" bind:checked={formState.largestProblemOnly} />
        Return largest problem only
      </label>

      <label>
        <input type="checkbox" bind:checked={formState.smallestProblemOnly} />
        Return smallest problem only
      </label>

      <label for="exclude-if-all"
        >Exclude if configs have <strong>all</strong> of</label
      >
      <textarea
        id="exclude-if-all"
        bind:value={formState.excludeIfConfigHasAllOf}
      />

      <label for="exclude-if-some"
        >Exclude if configs have <strong>some</strong> of</label
      >
      <textarea
        id="exclude-if-some"
        bind:value={formState.excludeIfConfigHasSomeOf}
      />

      <label for="include-if-all"
        >Include if configs have <strong>all</strong> of</label
      >
      <textarea
        id="include-if-all"
        bind:value={formState.includeIfConfigHasAllOf}
      />

      <label for="include-if-some"
        >Include if configs have <strong>some</strong> of</label
      >
      <textarea
        id="include-if-some"
        bind:value={formState.includeIfConfigHasSomeOf}
      />
    </Collapsible>

    <button on:click={fetchStatsOnly}> Fetch stats only </button>
    <button on:click={fetchStatsAndProblems}>
      Fetch stats and all problems
    </button>
  </form>

  {#if loading}
    <Stretch size="60" unit="px" color="#0d0d0d" />
  {/if}
  {#if !loading && response !== undefined}
    {#if !response.isComplete}
      <p>
        <strong>Warning:</strong> the database contains only a subset of problems of the queried problem family.
        Therefore, the results are not complete.
      </p>
    {/if}
    <Collapsible open={showStatistics} label={'Statistics:'}>
      <Statistics stats={response.stats} />
    </Collapsible>
    {#if !!response.problems}
      <Collapsible open={showProblems} label={'Problems:'}>
        <div class="problem-container">
          <VirtualList
            height="calc(100vh - 5em)"
            items={response.problems}
            let:item
          >
            <div class="problem-wrapper response">
              <p class="response-boldenned">Problem:</p>
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
              <p class="response-boldenned">Classification:</p>
              <Classification response={item} />
            </div>
          </VirtualList>
        </div>
      </Collapsible>
    {/if}
  {/if}
</div>

<style>
  .boldenned {
    font-weight: bold;
  }

  .problem-container {
    border-left: 2px solid rgb(228, 226, 226);
    /* border-right: 2px solid rgb(228, 226, 226); */
    border-bottom: 2px solid rgb(228, 226, 226);
  }
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
    margin: 5px;
  }

  li {
    margin: 0;
  }

  p {
    margin-bottom: 5px;
  }

  h5 {
    margin-bottom: 10px;
  }

  textarea {
    width: 250px;
    height: 100px;
  }
</style>
