from rooted_tree_classifier import is_log_star_solvable, is_log_solvable
from problem import GenericProblem
from parser import parseConfigs
from config_util import eachConstrIsHomogeneous, normalizeConstraints
from response import GenericResponse
from complexity import *
from .common import moveRootLabelToCenter

def classify(problem: GenericProblem) -> GenericResponse:
  if not problem.isTree:
    raise Exception('rooted-tree', 'Cannot classify if the problem is not a tree')

  if not problem.isRooted:
    raise Exception('rooted-tree', 'Cannot classify if the tree is not rooted')

  if not problem.isRegular:
    raise Exception('rooted-tree', 'Cannot classify if the graph is not regular')

  if not problem.rootAllowAll or not problem.leafAllowAll:
    raise Exception('rooted-tree', 'Leaves and roots must allow all configurations')

  parsedActives = parseConfigs(problem.activeConstraints)
  parsedPassives = parseConfigs(problem.passiveConstraints)

  activeDegree = len(parsedActives[0]) if len(parsedActives) else 3
  passiveDegree = len(parsedPassives[0]) if len(parsedPassives) else 2

  if activeDegree != 3:
    raise Exception('rooted-tree', 'Active configurations must be of size 3')

  if passiveDegree != 2:
    raise Exception('rooted-tree', 'Passive configurations must be of size 2')

  if not eachConstrIsHomogeneous(parsedPassives):
    raise Exception('rooted-tree', 'Passive constraints must be simple pairs of the same labels.')

  constraints = list(normalizeConstraints(parsedActives))
  constraints = [moveRootLabelToCenter(x) for x in constraints]

  detUpperBound = UNKNOWN
  detLowerBound = CONST
  randUpperBound = UNKNOWN
  randLowerBound = CONST
  if is_log_solvable(constraints):  # is not empty
    if is_log_star_solvable(constraints):
      detUpperBound = ITERATED_LOG
      randUpperBound = ITERATED_LOG
    else:
      detUpperBound = LOG
      detLowerBound = LOG
      randUpperBound = LOG
      randLowerBound = LOGLOG
  else:
    detLowerBound = GLOBAL
    randLowerBound = GLOBAL

  return GenericResponse(
    problem,
    randUpperBound,
    randLowerBound,
    detUpperBound,
    detLowerBound
  )
