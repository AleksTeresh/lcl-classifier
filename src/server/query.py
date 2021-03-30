from typing import List
from own_types import ComplexityType
from problem import ProblemProps
from complexity import *
from problem import parse_and_normalize


class QueryExcludeInclude:
    def __init__(
        self,
        exclude_if_config_has_all_of: List[str] = [],
        exclude_if_config_has_some_of: List[str] = [],
        include_if_config_has_all_of: List[str] = [],
        include_if_config_has_some_of: List[str] = [],
        return_largest_problem_only: bool = False,
        return_smallest_problem_only: bool = False,
        completely_rand_unclassifed_only: bool = False,
        partially_rand_unclassified_only: bool = False,
        completely_det_unclassifed_only: bool = False,
        partially_det_unclassified_only: bool = False,
    ):
        self.exclude_if_config_has_all_of = parse_and_normalize(
            exclude_if_config_has_all_of
        )
        self.exclude_if_config_has_some_of = parse_and_normalize(
            exclude_if_config_has_some_of
        )

        self.include_if_config_has_all_of = parse_and_normalize(
            include_if_config_has_all_of
        )
        self.include_if_config_has_some_of = parse_and_normalize(
            include_if_config_has_some_of
        )

        self.return_largest_problem_only = return_largest_problem_only
        self.return_smallest_problem_only = return_smallest_problem_only
        self.completely_rand_unclassifed_only = completely_rand_unclassifed_only
        self.partially_rand_unclassified_only = partially_rand_unclassified_only
        self.completely_det_unclassifed_only = completely_det_unclassifed_only
        self.partially_det_unclassified_only = partially_det_unclassified_only


class Bounds:
    def __init__(
        self,
        rand_upper_bound: ComplexityType = UNSOLVABLE,
        rand_lower_bound: ComplexityType = CONST,
        det_upper_bound: ComplexityType = UNSOLVABLE,
        det_lower_bound: ComplexityType = CONST,
    ):
        self.rand_upper_bound = rand_upper_bound
        self.rand_lower_bound = rand_lower_bound
        self.det_upper_bound = det_upper_bound
        self.det_lower_bound = det_lower_bound


class Query:
    def __init__(
        self,
        props: ProblemProps,
        exclude_include: QueryExcludeInclude = QueryExcludeInclude(),
        bounds: Bounds = Bounds(),
    ):
        self.bounds = bounds
        self.exclude_include = exclude_include
        self.props = props
