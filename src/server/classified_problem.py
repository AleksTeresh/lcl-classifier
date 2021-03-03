from typing import List
from problem import GenericProblem, ProblemFlags
from response import GenericResponse
from util import flatten

class ClassifiedProblem:
  def __init__(
    self,
    id: int,
    activeConstraints: List[str],
    passiveConstraints: List[str],
    leafConstraints: List[str],
    rootConstraints: List[str],
    isTree: bool,
    isCycle: bool,
    isPath: bool,
    isDirectedOrRooted: bool,
    isRegular: bool,
    randUpperBound,
    randLowerBound,
    detUpperBound,
    detLowerBound,
    solvableCount: str,
    unsolvableCount: str,
    papers,
    **kwargs
  ):
    self.id = id
    self.activeConstraints = activeConstraints
    self.passiveConstraints = passiveConstraints
    self.leafConstraints = leafConstraints
    self.rootConstraints = rootConstraints
    self.isTree = isTree
    self.isCycle = isCycle
    self.isPath = isPath
    self.isDirectedOrRooted = isDirectedOrRooted
    self.isRegular = isRegular
    self.randUpperBound = randUpperBound
    self.randLowerBound = randLowerBound
    self.detUpperBound = detUpperBound
    self.detLowerBound = detLowerBound
    self.solvableCount = solvableCount
    self.unsolvableCount = unsolvableCount
    self.papers = papers

  def toProblem(self) -> GenericProblem:
      p = GenericProblem(['A A'], ['A A'])
      p.id = self.id
      p.activeConstraints = self.activeConstraints
      p.passiveConstraints = self.passiveConstraints
      p.leafConstraints = self.leafConstraints
      p.rootConstraints = self.rootConstraints
      alphabet = p.getAlphabet()
      p.leafAllowAll = (set(flatten(p.leafConstraints)) - {' '}) == set(alphabet)
      p.rootAllowAll = (set(flatten(p.rootConstraints)) - {' '}) == set(alphabet)
      p.flags = ProblemFlags(
        isTree=self.isTree,
        isCycle=self.isCycle,
        isPath=self.isPath,
        isDirectedOrRooted=self.isDirectedOrRooted,
        isRegular=self.isRegular,
      )
      return p

  def toResponse(self) -> GenericResponse:
    return GenericResponse(
      problem = self.id,
      randUpperBound = self.randUpperBound,
      randLowerBound = self.randLowerBound,
      detUpperBound = self.detUpperBound,
      detLowerBound = self.detLowerBound,
      solvableCount = self.solvableCount,
      unsolvableCount = self.unsolvableCount,
      papers = self.papers
    )

