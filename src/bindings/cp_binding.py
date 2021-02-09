from problem import GenericProblem
from cyclepath_classifier import classify as cpClassify
from cyclepath_classifier import Problem as CyclePathProblem
from cyclepath_classifier import Type
from cyclepath_classifier import HARD
from cyclepath_classifier import CONST as CP_CONST
from cyclepath_classifier import GLOBAL as CP_GLOBAL
from cyclepath_classifier import ITERATED_LOG as CP_ITERATED_LOG
from cyclepath_classifier import UNSOLVABLE as CP_UNSOLVABLE
from parser import parseConfigs
from config_util import normalizeConstraints, eachConstrIsHomogeneous
from util import flatten
from response import GenericResponse
from complexity import *

def classify(problem: GenericProblem) -> GenericResponse:
  parsedActives = parseConfigs(problem.activeConstraints)
  parsedPassives = parseConfigs(problem.passiveConstraints)
  parsedRoots = parseConfigs(problem.rootConstraints)
  parsedLeaves = parseConfigs(problem.leafConstraints)

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

  edgeConstraints = set(normalizeConstraints(parsedPassives))
  nodeConstraints = {} if problemType == Type.TREE else set(normalizeConstraints(parsedActives))
  startConstraints = {} if problem.rootAllowAll else set(normalizeConstraints(parsedRoots))
  endConstraints = {} if problem.leafAllowAll else set(normalizeConstraints(parsedLeaves))

  cpProblem = CyclePathProblem(
    nodeConstraints,
    edgeConstraints,
    startConstraints,
    endConstraints,
    problemType
  )

  result = cpClassify(cpProblem)

  complexityMapping = {
    CP_CONST: CONST,
    CP_GLOBAL: GLOBAL,
    CP_ITERATED_LOG: ITERATED_LOG,
    CP_UNSOLVABLE: UNSOLVABLE
  }
  normalisedComplexity = complexityMapping[result['complexity']]

  return GenericResponse(
    problem,
    normalisedComplexity,
    normalisedComplexity,
    normalisedComplexity,
    normalisedComplexity,
    result['solvable'],
    result['unsolvable']
  )
  # print('Round complexity of the problem is %s' % result['complexity'])
  # print(
  #   'Deciding the number of solvable instances is NP-complete' if
  #   result['solvable'] == HARD else
  #   'There are %s solvable instances' % result['solvable']
  # )
  # print(
  #   'Deciding the number of unsolvable instances is NP-complete' if
  #   result['unsolvable'] == HARD else
  #   'There are %s unsolvable instances' % result['unsolvable']
  # )
