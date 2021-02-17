from problem import ProblemProps
from complexity import *

class QueryExcludeInclude:
  def __init__(
    self,
    excludeIfConfigHasAllOf = ['NOT_EXISTENT'],
    excludeIfConfigHasSomeOf = [],
    includeIfConfigHasAllOf = [],
    includeIfConfigHasSomeOf = [],
    returnLargestProblemOnly = False,
    returnSmallestProblemOnly = False,
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
    randUpperBound = UNSOLVABLE,
    randLowerBound = CONST,
    detUpperBound = UNSOLVABLE,
    detLowerBound = CONST
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

def fineResultsFile(query: Query):
  fileName = ''

def processQuery(query: Query):
  file = fineResultsFile(query)
  problems = getAllProblem(file)
  filtered = filterProblem(problems, query)
  return filtered
