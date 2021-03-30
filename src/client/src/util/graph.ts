import type { Problem } from '../types'

type HumanReadableGraphType = 'Tree' | 'Cycle' | 'Path'

export function getHumanReadableGraphType(
  problem: Problem
): HumanReadableGraphType {
  if (problem.flags.isTree) {
    return 'Tree'
  }
  if (problem.flags.isCycle) {
    return 'Cycle'
  }
  if (problem.flags.isPath) {
    return 'Path'
  }
  throw new Error('Unrecognized graph type')
}
