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
