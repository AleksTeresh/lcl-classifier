export enum Complexity {
  Const = '(1)',
  IteratedLog = '(log* n)',
  LogLog = '(loglog n)',
  Log = '(log n)',
  Global = '(n)',
  Unsolvable = 'unsolvable',
}
export interface Problem {
  activeConstraints: string[]
  passiveConstraints: string[]
  leafConstraints?: string[]
  rootConstraints?: string[]
  isTree: boolean
  isCycle: boolean
  isPath: boolean
}

export interface ClassifiedProblem extends Problem {
  activeConstraints: string[]
  passiveConstraints: string[]
  leafConstraints?: string[]
  rootConstraints?: string[]
  flags: {
    isTree: boolean
    isCycle: boolean
    isPath: boolean
  }
  detLowerBound: Complexity
  detUpperBound: Complexity
  randLowerBound: Complexity
  randUpperBound: Complexity
}

interface StatisticsComplexityData {
  randLowerBound: number
  detLowerBound: number
  randUpperBound: number
  detUpperBound: number
  randSolvable: number
  detSolvable: number
}

export interface QueryStatistics {
  const: StatisticsComplexityData
  logStar: StatisticsComplexityData
  logLog: StatisticsComplexityData
  log: StatisticsComplexityData
  linear: StatisticsComplexityData
  unsolvable: StatisticsComplexityData
  totalSize: number
}

export interface Query {
  isTree: boolean
  isCycle: boolean
  isPath: boolean
  isDirectedOrRooted: boolean
  isRegular: boolean

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
  excludeIfConfigHasAllOf: string[]
  excludeIfConfigHasSomeOf: string[]
  includeIfConfigHasAllOf: string[]
  includeIfConfigHasSomeOf: string[]
}

export type GraphType = 'tree' | 'cycle' | 'path'
