from problem import ProblemProps
from complexity import *
from config_util import parseAndNormalize


class QueryExcludeInclude:
    def __init__(
        self,
        excludeIfConfigHasAllOf=[],
        excludeIfConfigHasSomeOf=[],
        includeIfConfigHasAllOf=[],
        includeIfConfigHasSomeOf=[],
        returnLargestProblemOnly=False,
        returnSmallestProblemOnly=False,
        completelyRandUnclassifedOnly=False,
        partiallyRandUnclassifiedOnly=False,
        completelyDetUnclassifedOnly=False,
        partiallyDetUnclassifiedOnly=False,
    ):
        self.excludeIfConfigHasAllOf = tuple(parseAndNormalize(excludeIfConfigHasAllOf))
        self.excludeIfConfigHasSomeOf = tuple(
            parseAndNormalize(excludeIfConfigHasSomeOf)
        )
        self.includeIfConfigHasAllOf = tuple(parseAndNormalize(includeIfConfigHasAllOf))
        self.includeIfConfigHasSomeOf = tuple(
            parseAndNormalize(includeIfConfigHasSomeOf)
        )

        self.returnLargestProblemOnly = returnLargestProblemOnly
        self.returnSmallestProblemOnly = returnSmallestProblemOnly
        self.completelyRandUnclassifedOnly = completelyRandUnclassifedOnly
        self.partiallyRandUnclassifiedOnly = partiallyRandUnclassifiedOnly
        self.completelyDetUnclassifedOnly = completelyDetUnclassifedOnly
        self.partiallyDetUnclassifiedOnly = partiallyDetUnclassifiedOnly


class Bounds:
    def __init__(
        self,
        randUpperBound=UNSOLVABLE,
        randLowerBound=CONST,
        detUpperBound=UNSOLVABLE,
        detLowerBound=CONST,
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
