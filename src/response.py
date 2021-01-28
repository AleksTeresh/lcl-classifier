from complexity import *

class Paper:
  def __init__(self, name, authors, year, url):
    self.year = year
    self.name = name
    self.authors = authors
    self.url = url

class GenericResponse:
  def __init__(
    self,
    problem,
    randUpperBound = UNKNOWN,
    randLowerBound = CONST,
    detUpperBound = UNKNOWN,
    detLowerBound = CONST,
    solvableCount = "",
    unsolvableCount = "",
    papers = []
  ):
    self.problem = problem
    self.randUpperBound = randUpperBound
    self.randLowerBound = randLowerBound
    self.detUpperBound = detUpperBound
    self.detLowerBound = detLowerBound
    self.solvableCount = solvableCount
    self.unsolvableCount = unsolvableCount
    self.papers = papers

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
