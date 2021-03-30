<script lang="ts">
  /* eslint-env browser */
  import '../css/response.css'
  import { onMount } from 'svelte'
  import { Stretch } from 'svelte-loading-spinners'
  import VirtualList from '@sveltejs/svelte-virtual-list'
  import type { SvelteMouseEvent } from '../types'
  import Statistics from '../components/Statistics.svelte'
  import { readyQueries } from '../links/readyQueries'
  import Classification from '../components/Classification.svelte'
  import Collapsible from '../components/Collapsible.svelte'
  import ReturnedProblem from '../components/ReturnedProblem.svelte'
  import { getQueryResult, getTotalProblemCount } from '../api/api'
  import { persistStateToUrl, loadStateFromUrl } from '../urlStore'
  import type { Query, QueryResponse } from '../types'
  import { Complexity } from '../types'
  import type { QueryFormState as FormState } from './types'
  import { ExtendedQueryFormStateCodec as AugmentedFormStateCodec } from './types'

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
  let response: QueryResponse | undefined = undefined
  let problemCount: number | string = ''

  let showExcludeInclude = false
  let showComplexity = false
  let showStatistics = false
  let showProblems = false
  let showPremadeQueries = false
  let showExplanation = false

  onMount(async () => {
    const isProd: boolean = PRODUCTION
    const r = await getTotalProblemCount(isProd)
    if (r) {
      problemCount = r.problemCount
    }
    loading = false
    if (window.location.search.includes(`${FORM_PREFIX}_`)) {
      let augmentedFormState = {
        ...formState,
        fetchStatsOnly: true,
      }
      const parsedFormState = loadStateFromUrl(
        augmentedFormState,
        FORM_PREFIX,
        AugmentedFormStateCodec
      )
      if (parsedFormState === undefined) return

      augmentedFormState = parsedFormState
      formState = augmentedFormState
      const { fetchStatsOnly } = augmentedFormState
      const query = formStateToQuery(formState, { fetchStatsOnly })

      loading = true
      const isProd: boolean = PRODUCTION
      response = await getQueryResult(query, isProd)
      loading = false
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

  async function fetchStatsAndProblems(e: SvelteMouseEvent) {
    e.preventDefault()
    handleQuerySubmission(false)
  }

  async function fetchStatsOnly(e: SvelteMouseEvent) {
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
      <a target="_blank" href="https://zenodo.org/record/4601234">Zenodo</a>
    </p>

    <Collapsible open={showExplanation} label={'Explanation:'}>
      <p>
        The form below allows to query our database containing {problemCount}
        preclassifed problems. Alongside the problems satisfying the query, some
        statistics about the problems will be returned as well.
      </p>
    </Collapsible>

    <Collapsible
      open={showPremadeQueries}
      label={'Examples of interesting queries:'}
    >
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
        Active configs are monochromatic
      </label>

      <label>
        <input type="checkbox" bind:checked={formState.passivesAllSame} />
        Passive configs are monochromatic
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
        >Include only if configs have <strong>all</strong> of</label
      >
      <textarea
        id="include-if-all"
        bind:value={formState.includeIfConfigHasAllOf}
      />

      <label for="include-if-some"
        >Include only if configs have <strong>some</strong> of</label
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
        <strong>Warning:</strong> the database contains only a subset of problems
        of the queried problem family. Therefore, the results are not complete.
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
              <ReturnedProblem {item} />
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
</style>
