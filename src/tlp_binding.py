from problem import GenericProblem
from tlp_classifier import get_problem
from parser import parseConfigs
from config_util import normalizeConstraints

def classify(problem: GenericProblem):
  if problem.isCycle:
    raise Exception('tlp', 'Cannot classify if the graph is a cycle')

  if problem.isRooted:
    raise Exception('tlp', 'Cannot classify if the tree is rooted')

  if problem.isDirected:
    raise Exception('tlp', 'Cannot classify if the path is directed')

  if not problem.isRegular:
    raise Exception('tlp', 'Cannot classify if the graph is not regular')

  if not problem.rootAllowAll or not problem.leafAllowAll:
    raise Exception('tlp', 'Leaves and roots must allow all configurations')

  parsedActives = parseConfigs(problem.activeConstraints)
  parsedPassives = parseConfigs(problem.passiveConstraints)

  activeDegree = len(parsedActives[0]) if len(parsedActives) else 3
  passiveDegree = len(parsedPassives[0]) if len(parsedPassives) else 2

  if not (
    (activeDegree == 2 and passiveDegree == 2) or
    (activeDegree == 2 and passiveDegree == 3) or
    (activeDegree == 3 and passiveDegree == 2)):
    raise Exception('rooted-tree', 'Allowed degrees pairs are (2, 2), (2, 3), (3, 2)')

  activeConstraints = list(normalizeConstraints(parsedActives))
  passiveConstraints = list(normalizeConstraints(parsedPassives))

  result = get_problem(activeConstraints, passiveConstraints)
  print(result)
