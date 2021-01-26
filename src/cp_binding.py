from problem import GenericProblem
from cyclepath_classifier import classify as cpClassify, Problem as CyclePathProblem, Type, HARD
from parser import parseConfigs
from config_util import parseUnaryConstraints, parseBinaryConstraints, eachConstrIsHomogeneous
from util import flatten

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

  cpProblem = CyclePathProblem(
    nodeConstraints,
    edgeConstraints,
    startConstraints,
    endConstraints,
    problemType
  )

  result = cpClassify(cpProblem)

  print('Round complexity of the problem is %s' % result['complexity'])
  print(
    'Deciding the number of solvable instances is NP-complete' if
    result['solvable'] == HARD else
    'There are %s solvable instances' % result['solvable']
  )
  print(
    'Deciding the number of unsolvable instances is NP-complete' if
    result['unsolvable'] == HARD else
    'There are %s unsolvable instances' % result['unsolvable']
  )
