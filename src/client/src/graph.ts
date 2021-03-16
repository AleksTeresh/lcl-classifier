import type { ClassifiedProblem } from './types'

export function getGraphType(problem: ClassifiedProblem) {
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
