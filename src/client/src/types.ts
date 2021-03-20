import * as t from 'io-ts'
import { fromEnum } from './typeUtil'

export enum Complexity {
  Const = '(1)',
  IteratedLog = '(log* n)',
  LogLog = '(loglog n)',
  Log = '(log n)',
  Global = '(n)',
  Unsolvable = 'unsolvable',
}
export const ComplexityCodec = fromEnum<Complexity>('Complexity', Complexity)

const FlagsCodec = t.type(
  {
    isTree: t.boolean,
    isCycle: t.boolean,
    isPath: t.boolean,
  },
  'Flags'
)
export const ProblemCodec = t.type(
  {
    activeConstraints: t.array(t.string),
    passiveConstraints: t.array(t.string),
    leafConstraints: t.array(t.string),
    rootConstraints: t.array(t.string),
    flags: FlagsCodec,
  },
  'Problem'
)
export type Problem = t.TypeOf<typeof ProblemCodec>

const SourceCodec = t.type(
  {
    urls: t.array(t.string),
    name: t.string,
    shortName: t.string,
  },
  'Source'
)

export const SourcesCodec = t.type(
  {
    detLowerBoundSource: SourceCodec,
    detUpperBoundSource: SourceCodec,
    randLowerBoundSource: SourceCodec,
    randUpperBoundSource: SourceCodec,
  },
  'Sources'
)
export type Sources = t.TypeOf<typeof SourcesCodec>

export const ClassificationCodec = t.type(
  {
    detLowerBound: ComplexityCodec,
    detUpperBound: ComplexityCodec,
    randLowerBound: ComplexityCodec,
    randUpperBound: ComplexityCodec,
    papers: SourcesCodec,
  },
  'Classification'
)
export type Classification = t.TypeOf<typeof ClassificationCodec>

export const ClassifiedProblemCodec = t.intersection(
  [ProblemCodec, ClassificationCodec],
  'ClassifiedProblem'
)
export type ClassifiedProblem = t.TypeOf<typeof ClassifiedProblemCodec>

const StatisticsComplexityDataCodec = t.type(
  {
    randLowerBound: t.number,
    detLowerBound: t.number,
    randUpperBound: t.number,
    detUpperBound: t.number,
    randSolvable: t.number,
    detSolvable: t.number,
  },
  'StatisticsComplexityData'
)

export const QueryStatisticsCodec = t.type({
  const: StatisticsComplexityDataCodec,
  logStar: StatisticsComplexityDataCodec,
  logLog: StatisticsComplexityDataCodec,
  log: StatisticsComplexityDataCodec,
  linear: StatisticsComplexityDataCodec,
  unsolvable: StatisticsComplexityDataCodec,
  totalSize: t.number,
})
export type QueryStatistics = t.TypeOf<typeof QueryStatisticsCodec>

export const Query = t.type({
  isTree: t.boolean,
  isCycle: t.boolean,
  isPath: t.boolean,
  isDirectedOrRooted: t.boolean,

  randLowerBound: ComplexityCodec,
  randUpperBound: ComplexityCodec,
  detLowerBound: ComplexityCodec,
  detUpperBound: ComplexityCodec,

  activeDegree: t.number,
  passiveDegree: t.number,
  labelCount: t.number,
  activesAllSame: t.boolean,
  passivesAllSame: t.boolean,

  largestProblemOnly: t.boolean,
  smallestProblemOnly: t.boolean,
  completelyRandUnclassifiedOnly: t.boolean,
  partiallyRandUnclassifiedOnly: t.boolean,
  completelyDetUnclassifiedOnly: t.boolean,
  partiallyDetUnclassifiedOnly: t.boolean,
  excludeIfConfigHasAllOf: t.array(t.string),
  excludeIfConfigHasSomeOf: t.array(t.string),
  includeIfConfigHasAllOf: t.array(t.string),
  includeIfConfigHasSomeOf: t.array(t.string),
})
export type Query = t.TypeOf<typeof Query>

export const GraphTypeCodec = t.union(
  [t.literal('tree'), t.literal('cycle'), t.literal('path')],
  'GraphType'
)
export type GraphType = t.TypeOf<typeof GraphTypeCodec>

export const FindProblemResponseCodec = t.type(
  {
    result: ClassificationCodec,
    problem: ProblemCodec,
  },
  'FindProblemResponse'
)
export type FindProblemResponse = t.TypeOf<typeof FindProblemResponseCodec>

export const QueryResponseCodec = t.type(
  {
    problems: t.array(ClassifiedProblemCodec),
    stats: QueryStatisticsCodec,
    isComplete: t.boolean,
  },
  'QueryResponse'
)
export type QueryResponse = t.TypeOf<typeof QueryResponseCodec>

export const ProblemCountResponseCodec = t.type(
  {
    problemCount: t.number,
  },
  'ProblemCountResponse'
)
export type ProblemCountResponse = t.TypeOf<typeof ProblemCountResponseCodec>
