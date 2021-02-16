from file_util import getResultFilepath
from problem import ProblemFlags

class QueryExcludeInclude:
  def __init__(
    self,
    excludeIfConfigHasAllOf,
    excludeIfConfigHasSomeOf,
    includeIfConfigHasAllOf,
    includeIfConfigHasSomeOf,
    returnLargestProblemOnly,
    returnSmallestProblemOnly,
  ):
    self.excludeIfConfigHasAllOf = excludeIfConfigHasAllOf
    self.excludeIfConfigHasSomeOf = excludeIfConfigHasSomeOf

    self.includeIfConfigHasAllOf = includeIfConfigHasAllOf
    self.includeIfConfigHasSomeOf = includeIfConfigHasSomeOf

    self.returnLargestProblemOnly = returnLargestProblemOnly
    self.returnSmallestProblemOnly = returnSmallestProblemOnly

class Bounds:
  def __init__(
    self,
    randUpperBound,
    randLowerBound,
    detUpperBound,
    detLowerBound
  ):
    self.randUpperBound = randUpperBound
    self.randLowerBound = randLowerBound
    self.detUpperBound = detUpperBound
    self.detLowerBound = detLowerBound

class Query:
  def __init__(
    self,
    bounds: Bounds,
    excludeInclude: QueryExcludeInclude,
    flags: ProblemFlags,
    activeDegree=None,
    passiveDegree=None
  ):
    self.bounds = bounds
    self.excludeInclude = excludeInclude
    # partial properties of a problem e.g. isRegular, isTree, etc.
    self.flags = flags
    self.activeDegree = activeDegree
    self.passiveDegree = passiveDegree

def fineResultsFile(query: Query):
  fileName = ''

def processQuery(query: Query):
  file = fineResultsFile(query)
  problems = getAllProblem(file)
  filtered = filterProblem(problems, query)
  return filtered
