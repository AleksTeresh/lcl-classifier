<script>
  import ClassificationSource from './ClassificationSource.svelte'
  
  export let response
</script>

<p>
  Det. lower bound: {response.detLowerBound}
  <ClassificationSource
    source={response.papers.detLowerBoundSource} />
</p>
<p>
  Det. upper bound: {response.detUpperBound}
  <ClassificationSource
    source={response.papers.detUpperBoundSource} />
</p>
<p>
  Rand. lower bound: {response.randLowerBound}
  <ClassificationSource
    source={response.papers.randLowerBoundSource} />
</p>
<p>
  Rand. upper bound: {response.randUpperBound}
  <ClassificationSource
    source={response.papers.randUpperBoundSource} />
</p>
