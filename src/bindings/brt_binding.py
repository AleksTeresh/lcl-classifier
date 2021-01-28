from brt_classifier import getProblem
from brt_classifier import CONST as BRT_CONST
from brt_classifier import ITERATED_LOG as BRT_ITERATED_LOG
from brt_classifier import LOGLOG as BRT_LOGLOG
from brt_classifier import LOG as BRT_LOG
from brt_classifier import GLOBAL as BRT_GLOBAL
from brt_classifier import UNSOLVABLE as BRT_UNSOLVABLE
from brt_classifier import UNKNOWN as BRT_UNKNOWN
from problem import GenericProblem
from parser import parseConfigs
from config_util import eachConstrIsHomogeneous, normalizeConstraints
from .common import moveRootLabelToCenter
from util import flatten
from response import GenericResponse
from complexity import *

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

  complexityMapping = {
    BRT_CONST: CONST,
    BRT_ITERATED_LOG: ITERATED_LOG,
    BRT_LOGLOG: LOGLOG,
    BRT_LOG: LOG,
    BRT_GLOBAL: GLOBAL,
    BRT_UNSOLVABLE: UNSOLVABLE,
    BRT_UNKNOWN: UNKNOWN,
  }

  return GenericResponse(
    problem,
    complexityMapping[result['upper-bound']],
    complexityMapping[result['lower-bound']],
    UNKNOWN,
    complexityMapping[result['lower-bound']], # because randomised LB is also a deterministic LB
    result['solvable-count'],
    result['unsolvable-count']
  )

