<script lang="ts">
  import './response.css'
  import type { QueryStatistics } from './types'

  export let stats: QueryStatistics;
</script>

<div class="response">
  <p class="response-boldenned">Total # of problems: {stats.totalSize}</p>
  <p class="response-boldenned">Stats for randomised setting:</p>
  <p>Solvable in constant time: {stats.const.randSolvable}</p>
  <p>Solvable in log* time: {stats.logStar.randSolvable}</p>
  <p>Solvable in loglog time: {stats.logLog.randSolvable}</p>
  <p>Solvable in log time: {stats.log.randSolvable}</p>
  <p>Solvable in linear time: {stats.linear.randSolvable}</p>
  <p>Unsolvable: {stats.unsolvable.randSolvable}</p>
  <p>TBD: {(
    stats.totalSize -
    stats.const.randSolvable -
    stats.logStar.randSolvable -
    stats.logLog.randSolvable -
    stats.log.randSolvable -
    stats.linear.randSolvable -
    stats.unsolvable.randSolvable
  )}</p>

  <p class="response-boldenned">Lower bounds:</p>
  <p>Constant time: {stats.const.randLowerBound}</p>
  <p>Log* time: {stats.logStar.randLowerBound}</p>
  <p>Loglog time: {stats.logLog.randLowerBound}</p>
  <p>Log time: {stats.log.randLowerBound}</p>
  <p>Linear time: {stats.linear.randLowerBound}</p>
  <p>Unsolvable: {stats.unsolvable.randLowerBound}</p>
  <p>TBD: {(
    stats.totalSize -
    stats.const.randLowerBound -
    stats.logStar.randLowerBound -
    stats.logLog.randLowerBound -
    stats.log.randLowerBound -
    stats.linear.randLowerBound -
    stats.unsolvable.randLowerBound
  )}</p>

  <p class="response-boldenned">Upper bounds:</p>
  <p>Constant time: {stats.const.randUpperBound}</p>
  <p>Log* time: {stats.logStar.randUpperBound}</p>
  <p>Loglog time: {stats.logLog.randUpperBound}</p>
  <p>Log time: {stats.log.randUpperBound}</p>
  <p>Linear time: {stats.linear.randUpperBound}</p>
  <p>Unsolvable: {stats.unsolvable.randUpperBound}</p>
  <p>TBD: {(
    stats.totalSize -
    stats.const.randUpperBound -
    stats.logStar.randUpperBound -
    stats.logLog.randUpperBound -
    stats.log.randUpperBound -
    stats.linear.randUpperBound -
    stats.unsolvable.randUpperBound
  )}</p>
</div>

<style>
  .problem-wrapper {
    border-bottom: 1px solid black;
  }
</style>
