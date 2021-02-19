export enum Complexity {
  Const = '(1)',
  IteratedLog = '(log* n)',
  LogLog = '(loglog n)',
  Log = '(log n)',
  Global = '(n)',
  Unsolvable =  'unsolvable'
}
export interface Problem {
  activeConstraints: string[],
  passiveConstraints: string[],
  leafConstraints?: string[],
  rootConstraints?: string[],
  isTree: boolean,
  isCycle: boolean,
  isPath: boolean,
  isDirected: boolean,
  isRooted: boolean,
  isRegular: boolean,
}

export interface Query {
  isTree: boolean,
  isCycle: boolean,
  isPath: boolean,
  isDirected: boolean,
  isRooted: boolean,
  isRegular: boolean,
  
  randLowerBound: Complexity,
  randUpperBound: Complexity,
  detLowerBound: Complexity,
  detUpperBound: Complexity,
  
  activeDegree: number,
  passiveDegree: number,
  labelCount: number,
  activesAllSame: boolean,
  passivesAllSame: boolean,

  largestProblemOnly: boolean,
  smallestProblemOnly: boolean,
  excludeIfConfigHasAllOf: string[]
  excludeIfConfigHasSomeOf: string[]
  includeIfConfigHasAllOf: string[]
  includeIfConfigHasSomeOf: string[]
}
