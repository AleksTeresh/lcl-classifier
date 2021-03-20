<script lang="ts">
  import ClassificationSource from "./ClassificationSource.svelte"
  import type { Classification } from './types'

  export let response: Classification
</script>

<p>
  Det. lower bound: {response.detLowerBound}
  <ClassificationSource
    lowerBound={response.detLowerBound}
    source={response.papers.detLowerBoundSource} />
</p>
<p>
  Det. upper bound: {response.detUpperBound}
  <ClassificationSource
    upperBound={response.detUpperBound}
    source={response.papers.detUpperBoundSource} />
</p>
<p>
  Rand. lower bound: {response.randLowerBound}
  <ClassificationSource
    lowerBound={response.randLowerBound}
    source={response.papers.randLowerBoundSource} />
</p>
<p>
  Rand. upper bound: {response.randUpperBound}
  <ClassificationSource
    upperBound={response.randUpperBound}
    source={response.papers.randUpperBoundSource} />
</p>
