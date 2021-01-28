from brt_classifier import getProblem
from problem import GenericProblem
from parser import parseConfigs
from config_util import eachConstrIsHomogeneous, normalizeConstraints
from rt_binding import moveRootLabelToCenter
from util import flatten

def classify(problem: GenericProblem):
  if not problem.isTree:
    raise Exception('brt', 'Cannot classify if the problem is not a tree')

  if not problem.isRooted:
    raise Exception('brt', 'Cannot classify if the tree is not rooted')

  if not problem.isRegular:
    raise Exception('brt', 'Cannot classify if the graph is not regular')

  if not problem.rootAllowAll or not problem.leafAllowAll:
    raise Exception('brt', 'Leaves and roots must allow all configurations')

  parsedActives = parseConfigs(problem.activeConstraints)
  parsedPassives = parseConfigs(problem.passiveConstraints)

  activeDegree = len(parsedActives[0]) if len(parsedActives) else 3
  passiveDegree = len(parsedPassives[0]) if len(parsedPassives) else 2

  if activeDegree != 3:
    raise Exception('brt', 'Active configurations must be of size 3')

  if passiveDegree != 2:
    raise Exception('brt', 'Passive configurations must be of size 2')

  if not eachConstrIsHomogeneous(parsedPassives):
    raise Exception('brt', 'Passive constraints must be simple pairs of the same labels.')

  constraints = list(normalizeConstraints(parsedActives))
  constraints = [moveRootLabelToCenter(x) for x in constraints]

  alphabet = set(flatten(constraints))

  for i, label in enumerate(alphabet):
    constraints = [x.replace(label, str(i+1)) for x in constraints]
  
  result = getProblem(constraints)
  print(result)
