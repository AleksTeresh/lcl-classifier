
class Query:
  def __init__(
    self,
    randUpperBound,
    randLowerBound,
    detUpperBound,
    detLowerBound,
    excludeIfConfigHasAllOf,
    excludeIfConfigHasSomeOf,
    includeIfConfigHasAllOf,
    includeIfConfigHasSomeOf,
    returnLargestProblemOnly,
    returnSmallestProblemOnly
  ):
    self.randUpperBound = randUpperBound
    self.randLowerBound = randLowerBound
    self.detUpperBound = detUpperBound
    self.detLowerBound = detLowerBound
    
    self.excludeIfConfigHasAllOf = excludeIfConfigHasAllOf
    self.excludeIfConfigHasSomeOf = excludeIfConfigHasSomeOf

    self.includeIfConfigHasAllOf = includeIfConfigHasAllOf
    self.includeIfConfigHasSomeOf = includeIfConfigHasSomeOf

    self.returnLargestProblemOnly = returnLargestProblemOnly
    self.returnSmallestProblemOnly = returnSmallestProblemOnly
