from typing import List, Union
from own_types import ComplexityType
from problem import GenericProblem
from complexity import *


class Source:
    def __init__(self, shortName: str, name: str, urls: List[str]):
        self.shortName = shortName
        self.name = name
        self.urls = urls


class Sources:
    def __init__(
        self,
        randUpperBoundSource: Source = None,
        randLowerBoundSource: Source = None,
        detUpperBoundSource: Source = None,
        detLowerBoundSource: Source = None,
    ):
        self.randUpperBoundSource = randUpperBoundSource
        self.randLowerBoundSource = randLowerBoundSource
        self.detUpperBoundSource = detUpperBoundSource
        self.detLowerBoundSource = detLowerBoundSource

    def getRUBSource(self):
        return (
            self.randUpperBoundSource.shortName
            if self.randUpperBoundSource is not None
            else None
        )

    def getRLBSource(self):
        return (
            self.randLowerBoundSource.shortName
            if self.randLowerBoundSource is not None
            else None
        )

    def getDUBSource(self):
        return (
            self.detUpperBoundSource.shortName
            if self.detUpperBoundSource is not None
            else None
        )

    def getDLBSource(self):
        return (
            self.detLowerBoundSource.shortName
            if self.detLowerBoundSource is not None
            else None
        )

    def dict(self):
        return {
            "randUpperBoundSource": self.randUpperBoundSource.__dict__
            if self.randUpperBoundSource is not None
            else None,
            "randLowerBoundSource": self.randLowerBoundSource.__dict__
            if self.randLowerBoundSource is not None
            else None,
            "detUpperBoundSource": self.detUpperBoundSource.__dict__
            if self.detUpperBoundSource is not None
            else None,
            "detLowerBoundSource": self.detLowerBoundSource.__dict__
            if self.detLowerBoundSource is not None
            else None,
        }


class GenericResponse:
    def __init__(
        self,
        problem: Union[GenericProblem, int],
        randUpperBound: ComplexityType = UNSOLVABLE,
        randLowerBound: ComplexityType = CONST,
        detUpperBound: ComplexityType = UNSOLVABLE,
        detLowerBound: ComplexityType = CONST,
        solvableCount: str = "",
        unsolvableCount: str = "",
        papers: Sources = Sources(),
    ):
        self.problem = problem
        self.randUpperBound = randUpperBound
        self.randLowerBound = randLowerBound
        self.detUpperBound = detUpperBound
        self.detLowerBound = detLowerBound
        self.solvableCount = solvableCount
        self.unsolvableCount = unsolvableCount
        self.papers = papers

    def dict(self):
        return {
            "randUpperBound": self.randUpperBound,
            "randLowerBound": self.randLowerBound,
            "detUpperBound": self.detUpperBound,
            "detLowerBound": self.detLowerBound,
            "solvableCount": self.solvableCount,
            "unsolvableCount": self.unsolvableCount,
            "papers": self.papers.dict(),
        }

    def __repr__(self):
        return "Rand. UB: %s\n\
Rand. LB: %s\n\
Det. UB: %s\n\
Det. LB: %s\n" % (
            self.randUpperBound,
            self.randLowerBound,
            self.detUpperBound,
            self.detLowerBound,
        )
