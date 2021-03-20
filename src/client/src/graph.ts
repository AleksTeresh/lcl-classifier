import type { Problem } from './types'

export function getGraphType(problem: Problem) {
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
