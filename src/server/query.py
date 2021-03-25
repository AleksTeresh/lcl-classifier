from typing import List
from own_types import ComplexityType
from problem import ProblemProps
from complexity import *
from problem import parseAndNormalize


class QueryExcludeInclude:
    def __init__(
        self,
        excludeIfConfigHasAllOf: List[str] = [],
        excludeIfConfigHasSomeOf: List[str] = [],
        includeIfConfigHasAllOf: List[str] = [],
        includeIfConfigHasSomeOf: List[str] = [],
        returnLargestProblemOnly: bool = False,
        returnSmallestProblemOnly: bool = False,
        completelyRandUnclassifedOnly: bool = False,
        partiallyRandUnclassifiedOnly: bool = False,
        completelyDetUnclassifedOnly: bool = False,
        partiallyDetUnclassifiedOnly: bool = False,
    ):
        self.excludeIfConfigHasAllOf = parseAndNormalize(excludeIfConfigHasAllOf)
        self.excludeIfConfigHasSomeOf = parseAndNormalize(excludeIfConfigHasSomeOf)

        self.includeIfConfigHasAllOf = parseAndNormalize(includeIfConfigHasAllOf)
        self.includeIfConfigHasSomeOf = parseAndNormalize(includeIfConfigHasSomeOf)

        self.returnLargestProblemOnly = returnLargestProblemOnly
        self.returnSmallestProblemOnly = returnSmallestProblemOnly
        self.completelyRandUnclassifedOnly = completelyRandUnclassifedOnly
        self.partiallyRandUnclassifiedOnly = partiallyRandUnclassifiedOnly
        self.completelyDetUnclassifedOnly = completelyDetUnclassifedOnly
        self.partiallyDetUnclassifiedOnly = partiallyDetUnclassifiedOnly


class Bounds:
    def __init__(
        self,
        randUpperBound: ComplexityType = UNSOLVABLE,
        randLowerBound: ComplexityType = CONST,
        detUpperBound: ComplexityType = UNSOLVABLE,
        detLowerBound: ComplexityType = CONST,
    ):
        self.randUpperBound = randUpperBound
        self.randLowerBound = randLowerBound
        self.detUpperBound = detUpperBound
        self.detLowerBound = detLowerBound


class Query:
    def __init__(
        self,
        props: ProblemProps,
        excludeInclude: QueryExcludeInclude = QueryExcludeInclude(),
        bounds: Bounds = Bounds(),
    ):
        self.bounds = bounds
        self.excludeInclude = excludeInclude
        self.props = props
