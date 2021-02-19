from functools import reduce
from itertools import product
from util import flatMap, flatten, areAllTheSame
from parser import parseConfigs

def flattenBinaryConfigs(left, right):
  return [l + r for l in left for r in right]

def flattenTernaryConfigs(one, two, three):
  return [o + tw + th for o in one for tw in two for th in three]

def flattenConfigs(configs):
  if len(configs) == 1:
    return flatten(configs)
  elif len(configs) == 2:
    return flattenBinaryConfigs(configs[0], configs[1])
  elif len(configs) == 3:
    return flattenTernaryConfigs(configs[0], configs[1], configs[2])
  else:
    return ["".join(x) for x in product(*configs)]

def normalizeConstraints(constr):
  return flatMap(lambda x: flattenConfigs(x), constr)

def parseAndNormalize(constr):
  constr = parseConfigs(constr)
  constr = list(normalizeConstraints(constr))
  return constr

def eachConstrIsHomogeneous(constrs):
  return reduce(lambda acc, x: acc and areAllTheSame(flatten(x)), constrs, True)