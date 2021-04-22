from typing import List
from own_types import ComplexityType
from problem import GenericProblem
from complexity import UNSOLVABLE, CONST


class Source:
    def __init__(self, short_name: str, name: str, urls: List[str]):
        self.short_name = short_name
        self.name = name
        self.urls = urls


class Sources:
    def __init__(
        self,
        rand_upper_bound_source: Source = None,
        rand_lower_bound_source: Source = None,
        det_upper_bound_source: Source = None,
        det_lower_bound_source: Source = None,
    ):
        self.rand_upper_bound_source = rand_upper_bound_source
        self.rand_lower_bound_source = rand_lower_bound_source
        self.det_upper_bound_source = det_upper_bound_source
        self.det_lower_bound_source = det_lower_bound_source

    def get_rub_source(self):
        return (
            self.rand_upper_bound_source.short_name
            if self.rand_upper_bound_source is not None
            else None
        )

    def get_rlb_source(self):
        return (
            self.rand_lower_bound_source.short_name
            if self.rand_lower_bound_source is not None
            else None
        )

    def get_dub_source(self):
        return (
            self.det_upper_bound_source.short_name
            if self.det_upper_bound_source is not None
            else None
        )

    def get_dlb_source(self):
        return (
            self.det_lower_bound_source.short_name
            if self.det_lower_bound_source is not None
            else None
        )

    def dict(self):
        return {
            "rand_upper_bound_source": self.rand_upper_bound_source.__dict__
            if self.rand_upper_bound_source is not None
            else None,
            "rand_lower_bound_source": self.rand_lower_bound_source.__dict__
            if self.rand_lower_bound_source is not None
            else None,
            "det_upper_bound_source": self.det_upper_bound_source.__dict__
            if self.det_upper_bound_source is not None
            else None,
            "det_lower_bound_source": self.det_lower_bound_source.__dict__
            if self.det_lower_bound_source is not None
            else None,
        }


class GenericResponse:
    def __init__(
        self,
        problem: GenericProblem,
        rand_upper_bound: ComplexityType = UNSOLVABLE,
        rand_lower_bound: ComplexityType = CONST,
        det_upper_bound: ComplexityType = UNSOLVABLE,
        det_lower_bound: ComplexityType = CONST,
        solvable_count: str = "",
        unsolvable_count: str = "",
        papers: Sources = Sources(),
    ):
        self.problem = problem
        self.rand_upper_bound = rand_upper_bound
        self.rand_lower_bound = rand_lower_bound
        self.det_upper_bound = det_upper_bound
        self.det_lower_bound = det_lower_bound
        self.solvable_count = solvable_count
        self.unsolvable_count = unsolvable_count
        self.papers = papers

    def dict(self):
        return {
            "rand_upper_bound": self.rand_upper_bound,
            "rand_lower_bound": self.rand_lower_bound,
            "det_upper_bound": self.det_upper_bound,
            "det_lower_bound": self.det_lower_bound,
            "solvable_count": self.solvable_count,
            "unsolvable_count": self.unsolvable_count,
            "papers": self.papers.dict(),
        }

    def __repr__(self):
        return "Rand. UB: %s\n\
Rand. LB: %s\n\
Det. UB: %s\n\
Det. LB: %s\n" % (
            self.rand_upper_bound,
            self.rand_lower_bound,
            self.det_upper_bound,
            self.det_lower_bound,
        )

    def __lt__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.problem < other.problem
        else:
            return False
