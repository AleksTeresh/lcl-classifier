from problem import GenericProblem
from cyclepath_classifier import classify as cpClassify, Problem as CyclePathProblem, Type
from parser import parseConfigs
from util import flatMap

def flattenBinaryConfigs(left, right):
  return [l + r for l in left for r in right]

def parseUnaryConstraints(constr):
  return flatMap(lambda x: x, flatMap(lambda x: x, constr))

def parseBinaryConstraints(constr):
  return flatMap(lambda x: flattenBinaryConfigs(x[0], x[1]), constr)

def classify(problem: GenericProblem):
  parsedActives = parseConfigs(problem.activeConstraints)
  parsedPassives = parseConfigs(problem.passiveConstraints)
  parsedRoots = parseConfigs(problem.rootConstraints)
  parsedLeaves = parseConfigs(problem.leafConstraints)

  # TODO: handle allowAllActive, allowAllPassive

  # TODO: check that leaf degree is 1 and (root degree is 1)

  activeDegree = len(parsedActives[0])
  passiveDegree = len(parsedPassives[0])

  if passiveDegree != 2:
    raise Exception('cyclepath', 'Passive constraints must always be of degree 2')

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
  
