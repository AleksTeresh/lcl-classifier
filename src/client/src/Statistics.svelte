<script lang="ts">
  import "./response.css"
  import type { QueryStatistics } from "./types"

  export let stats: QueryStatistics
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
  <p>
    TBD: {stats.totalSize -
      stats.const.randSolvable -
      stats.logStar.randSolvable -
      stats.logLog.randSolvable -
      stats.log.randSolvable -
      stats.linear.randSolvable -
      stats.unsolvable.randSolvable}
  </p>

  <p class="response-boldenned">Lower bounds:</p>
  <p>Constant time: {stats.const.randLowerBound}</p>
  <p>Log* time: {stats.logStar.randLowerBound}</p>
  <p>Loglog time: {stats.logLog.randLowerBound}</p>
  <p>Log time: {stats.log.randLowerBound}</p>
  <p>Linear time: {stats.linear.randLowerBound}</p>
  <p>Unsolvable: {stats.unsolvable.randLowerBound}</p>

  <p class="response-boldenned">Upper bounds:</p>
  <p>Constant time: {stats.const.randUpperBound}</p>
  <p>Log* time: {stats.logStar.randUpperBound}</p>
  <p>Loglog time: {stats.logLog.randUpperBound}</p>
  <p>Log time: {stats.log.randUpperBound}</p>
  <p>Linear time: {stats.linear.randUpperBound}</p>
  <p>Unsolvable: {stats.unsolvable.randUpperBound}</p>

  <p class="response-boldenned">Stats for deterministic setting:</p>
  <p>Solvable in constant time: {stats.const.detSolvable}</p>
  <p>Solvable in log* time: {stats.logStar.detSolvable}</p>
  <p>Solvable in loglog time: {stats.logLog.detSolvable}</p>
  <p>Solvable in log time: {stats.log.detSolvable}</p>
  <p>Solvable in linear time: {stats.linear.detSolvable}</p>
  <p>Unsolvable: {stats.unsolvable.detSolvable}</p>
  <p>
    TBD: {stats.totalSize -
      stats.const.detSolvable -
      stats.logStar.detSolvable -
      stats.logLog.detSolvable -
      stats.log.detSolvable -
      stats.linear.detSolvable -
      stats.unsolvable.detSolvable}
  </p>

  <p class="response-boldenned">Lower bounds:</p>
  <p>Constant time: {stats.const.detLowerBound}</p>
  <p>Log* time: {stats.logStar.detLowerBound}</p>
  <p>Loglog time: {stats.logLog.detLowerBound}</p>
  <p>Log time: {stats.log.detLowerBound}</p>
  <p>Linear time: {stats.linear.detLowerBound}</p>
  <p>Unsolvable: {stats.unsolvable.detLowerBound}</p>

  <p class="response-boldenned">Upper bounds:</p>
  <p>Constant time: {stats.const.detUpperBound}</p>
  <p>Log* time: {stats.logStar.detUpperBound}</p>
  <p>Loglog time: {stats.logLog.detUpperBound}</p>
  <p>Log time: {stats.log.detUpperBound}</p>
  <p>Linear time: {stats.linear.detUpperBound}</p>
  <p>Unsolvable: {stats.unsolvable.detUpperBound}</p>
</div>
