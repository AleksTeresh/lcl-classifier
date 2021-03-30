import * as t from 'io-ts'
import { GraphTypeCodec, ComplexityCodec } from '../types'

export const ProblemFormStateCodec = t.type(
  {
    activeConstraints: t.string,
    passiveConstraints: t.string,
    leafConstraints: t.union([t.string, t.undefined]),
    rootConstraints: t.union([t.string, t.undefined]),
    graphType: GraphTypeCodec,
  },
  'ProblemFormState'
)

export type ProblemFormState = t.TypeOf<typeof ProblemFormStateCodec>

const QueryFormStateCodec = t.type(
  {
    graphType: GraphTypeCodec,
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
    excludeIfConfigHasAllOf: t.string,
    excludeIfConfigHasSomeOf: t.string,
    includeIfConfigHasAllOf: t.string,
    includeIfConfigHasSomeOf: t.string,
  },
  'QueryFormState'
)
export const ExtendedQueryFormStateCodec = t.intersection(
  [
    QueryFormStateCodec,
    t.type({
      fetchStatsOnly: t.boolean,
    }),
  ],
  'ExtendedQueryFormStateCodec'
)

export type QueryFormState = t.TypeOf<typeof QueryFormStateCodec>
export type ExtendedQueryFormState = t.TypeOf<
  typeof ExtendedQueryFormStateCodec
>
