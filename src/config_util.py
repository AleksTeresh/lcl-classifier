from functools import reduce
from util import flatMap, flatten, areAllTheSame

def flattenBinaryConfigs(left, right):
  return [l + r for l in left for r in right]

def flattenTernaryConfigs(one, two, three):
  return [o + tw + th for o in one for tw in two for th in three]

def parseUnaryConstraints(constr):
  return flatten(flatten(constr))

def parseBinaryConstraints(constr):
  return flatMap(lambda x: flattenBinaryConfigs(x[0], x[1]), constr)

def parseTernaryConstraints(constr):
  return flatMap(lambda x: flattenTernaryConfigs(x[0], x[1], x[2]), constr)

def eachConstrIsHomogeneous(constrs):
  return reduce(lambda acc, x: acc and areAllTheSame(flatten(x)), constrs, True)
