import * as t from 'io-ts'

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
  flags: {
    isTree: boolean
    isCycle: boolean
    isPath: boolean
  }
}

export interface Sources {
  detLowerBound: Complexity
  detUpperBound: Complexity
  randLowerBound: Complexity
  randUpperBound: Complexity
}

export interface Classification {
  detLowerBound: Complexity
  detUpperBound: Complexity
  randLowerBound: Complexity
  randUpperBound: Complexity
  papers: Sources
}

export type ClassifiedProblem = Problem & Classification

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

export interface FindProblemResponse {
  result: Classification,
  problem: Problem
}

export interface QueryResponse {
  problems: ClassifiedProblem[]
  stats: QueryStatistics
  isComplete: boolean
}

export interface ProblemCountResponse {
  problemCount: number
}
