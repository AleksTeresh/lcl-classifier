from typing import List
from own_types import ConfigType
from problem import unparse_configs
from problem import GenericProblem, ProblemFlags
from response import GenericResponse
from util import flatten


class ClassifiedProblem:
    def __init__(
        self,
        id: int,
        active_constraints: ConfigType,
        passive_constraints: ConfigType,
        leaf_constraints: ConfigType,
        root_constraints: ConfigType,
        is_tree: bool,
        is_cycle: bool,
        is_path: bool,
        is_directed_or_rooted: bool,
        is_regular: bool,
        rand_upper_bound,
        rand_lower_bound,
        det_upper_bound,
        det_lower_bound,
        solvable_count: str,
        unsolvable_count: str,
        papers,
        **kwargs
    ):
        self.id = id
        self.active_constraints = active_constraints
        self.passive_constraints = passive_constraints
        self.leaf_constraints = leaf_constraints
        self.root_constraints = root_constraints
        self.is_tree = is_tree
        self.is_cycle = is_cycle
        self.is_path = is_path
        self.is_directed_or_rooted = is_directed_or_rooted
        self.is_regular = is_regular
        self.rand_upper_bound = rand_upper_bound
        self.rand_lower_bound = rand_lower_bound
        self.det_upper_bound = det_upper_bound
        self.det_lower_bound = det_lower_bound
        self.solvable_count = solvable_count
        self.unsolvable_count = unsolvable_count
        self.papers = papers

    def to_problem(self) -> GenericProblem:
        p = GenericProblem(["A A"], ["A A"])
        p.id = self.id
        p.active_constraints = self.active_constraints
        p.passive_constraints = self.passive_constraints
        p.leaf_constraints = self.leaf_constraints
        p.root_constraints = self.root_constraints
        alphabet = p.get_alphabet()
        p.leaf_allow_all = (set(flatten(p.leaf_constraints)) - {" "}) == set(alphabet)
        p.root_allow_all = (set(flatten(p.root_constraints)) - {" "}) == set(alphabet)
        p.flags = ProblemFlags(
            is_tree=self.is_tree,
            is_cycle=self.is_cycle,
            is_path=self.is_path,
            is_directed_or_rooted=self.is_directed_or_rooted,
            is_regular=self.is_regular,
        )
        return p

    def to_unparsed_problem(self):
        p = self.to_problem()
        p.active_constraints = unparse_configs(
            p.active_constraints, p.flags.is_directed_or_rooted
        )
        p.passive_constraints = unparse_configs(
            p.passive_constraints, p.flags.is_directed_or_rooted
        )
        p.root_constraints = unparse_configs(
            p.root_constraints, p.flags.is_directed_or_rooted
        )
        p.leaf_constraints = unparse_configs(
            p.leaf_constraints, p.flags.is_directed_or_rooted
        )
        return p

    def to_response(self) -> GenericResponse:
        return GenericResponse(
            problem=self.to_problem(),
            rand_upper_bound=self.rand_upper_bound,
            rand_lower_bound=self.rand_lower_bound,
            det_upper_bound=self.det_upper_bound,
            det_lower_bound=self.det_lower_bound,
            solvable_count=self.solvable_count,
            unsolvable_count=self.unsolvable_count,
            papers=self.papers,
        )
