from complexity import *

class Source:
  def __init__(
    self,
    name,
    urls
  ):
    self.name = name
    self.urls = urls
class Sources:
  def __init__(
    self,
    randUpperBoundSource = None,
    randLowerBoundSource = None,
    detUpperBoundSource = None,
    detLowerBoundSource = None
  ):
    self.randUpperBoundSource = randUpperBoundSource
    self.randLowerBoundSource = randLowerBoundSource
    self.detUpperBoundSource = detUpperBoundSource
    self.detLowerBoundSource = detLowerBoundSource

  def dict(self):
    return {
      "randUpperBoundSource": self.randUpperBoundSource,
      "randLowerBoundSource": self.randLowerBoundSource,
      "detUpperBoundSource": self.detUpperBoundSource,
      "detLowerBoundSource": self.detLowerBoundSource
    }

class GenericResponse:
  def __init__(
    self,
    problem,
    randUpperBound = UNSOLVABLE,
    randLowerBound = CONST,
    detUpperBound = UNSOLVABLE,
    detLowerBound = CONST,
    solvableCount = "",
    unsolvableCount = "",
    papers: Sources = Sources()
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
      "papers": self.papers.dict()
    }

  def __repr__(self):
    return "Rand. UB: %s\n\
Rand. LB: %s\n\
Det. UB: %s\n\
Det. LB: %s\n"%(
  self.randUpperBound,
  self.randLowerBound,
  self.detUpperBound,
  self.detLowerBound
)  
    
