from functools import reduce
from problem import GenericProblem
from cyclepath_classifier import classify as cpClassify, Problem as CyclePathProblem, Type
from parser import parseConfigs
from util import flatMap, flatten, areAllTheSame

def flattenBinaryConfigs(left, right):
  return [l + r for l in left for r in right]

def parseUnaryConstraints(constr):
  return flatten(flatten(constr))

def parseBinaryConstraints(constr):
  return flatMap(lambda x: flattenBinaryConfigs(x[0], x[1]), constr)

def eachConstrIsHomogeneous(constrs):
  return reduce(lambda acc, x: acc and areAllTheSame(flatten(x)), constrs, True)

def classify(problem: GenericProblem):
  parsedActives = parseConfigs(problem.activeConstraints)
  parsedPassives = parseConfigs(problem.passiveConstraints)
  parsedRoots = parseConfigs(problem.rootConstraints)
  parsedLeaves = parseConfigs(problem.leafConstraints)

  # TODO: handle allowAllActive, allowAllPassive

  activeDegree = len(parsedActives[0]) if len(parsedActives) else 2
  passiveDegree = len(parsedPassives[0]) if len(parsedPassives) else 2
  leafDegree = len(parsedLeaves[0]) if len(parsedLeaves) else 1

  if leafDegree != 1:
    raise Exception('cyclepath', 'Leaf constraints must always be of degree 1')

  if passiveDegree != 2:
    raise Exception('cyclepath', 'Passive constraints must always be of degree 2')

  if problem.isTree:
    if not eachConstrIsHomogeneous(parsedActives):
      raise Exception('cyclepath', 'On trees, node constraints must be the same for all incident edges.')
  elif activeDegree != 2:
    raise Exception('cyclepath', 'In a path or cycle, passive constraints must always be of degree 2')

  problemType = Type.TREE if problem.isTree else (Type.DIRECTED if problem.isDirected else Type.UNDIRECTED)    

  edgeConstraints = set(parseBinaryConstraints(parsedPassives))
  nodeConstraints = {} if problemType == Type.TREE else set(parseBinaryConstraints(parsedActives))
  startConstraints = {} if problem.rootAllowAll else set(parseUnaryConstraints(parsedRoots))
  endConstraints = {} if problem.leafAllowAll else set(parseUnaryConstraints(parsedLeaves))

  # TODO: move this part to the classifier package itself
  if problemType == Type.TREE:
    alphabet = set(flatMap(lambda x: x, edgeConstraints))
    nodeConstraints = set(map(lambda x: x + x, alphabet))
    startConstraints = alphabet
    endConstraints = alphabet

  # print(edgeConstraints)
  # print(nodeConstraints)
  # print(startConstraints)
  # print(endConstraints)

  cpProblem = CyclePathProblem(
    nodeConstraints,
    edgeConstraints,
    startConstraints,
    endConstraints,
    problemType
  )
  cpClassify(cpProblem)
  
