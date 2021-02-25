from typing import List
from brt_classifier import getProblem, getProblems
from brt_classifier import CONST as BRT_CONST
from brt_classifier import ITERATED_LOG as BRT_ITERATED_LOG
from brt_classifier import LOGLOG as BRT_LOGLOG
from brt_classifier import LOG as BRT_LOG
from brt_classifier import GLOBAL as BRT_GLOBAL
from brt_classifier import UNSOLVABLE as BRT_UNSOLVABLE
from brt_classifier import UNKNOWN as BRT_UNKNOWN
from problem import GenericProblem
from config_util import eachConstrIsHomogeneous, normalizeConstraints
from .common import moveRootLabelToCenter
from util import flatten
from classifier import ClassifyContext
from response import GenericResponse
from complexity import *

complexityMapping = {
    BRT_CONST: CONST,
    BRT_ITERATED_LOG: ITERATED_LOG,
    BRT_LOGLOG: LOGLOG,
    BRT_LOG: LOG,
    BRT_GLOBAL: GLOBAL,
    BRT_UNSOLVABLE: UNSOLVABLE,
    BRT_UNKNOWN: UNKNOWN,
  }

def preprocessProblem(p):
  alphabet = p.getAlphabet()
  constraints = [moveRootLabelToCenter(x) for x in p.activeConstraints]

  for i, label in enumerate(alphabet):
    constraints = [x.replace(label, str(i+1)) for x in constraints]
  return constraints

def batchClassify(ps: List[GenericProblem]):
  representativeP = ps[0]
  try:
    classify(representativeP)
  except Exception as e:
    print(e)
    raise Exception('Cannot batch classify')

  constrs = [preprocessProblem(p) for p in ps]

  results = getProblems(
    constrs,
    len(set(flatten(flatten(constrs))))
  )

  return [
    GenericResponse(
      ps[i],
      complexityMapping[r['upper-bound']],
      complexityMapping[r['lower-bound']],
      UNSOLVABLE,
      complexityMapping[r['lower-bound']], # because randomised LB is also a deterministic LB
      r['solvable-count'],
      r['unsolvable-count']
    ) for i, r in enumerate(results)
  ]

def classify(
  p: GenericProblem,
  context: ClassifyContext = ClassifyContext()
) -> GenericResponse:
  if context.brtPreclassified:
    return GenericResponse(p)

  if not p.flags.isTree:
    raise Exception('brt', 'Cannot classify if the problem is not a tree')

  if not p.flags.isRooted:
    raise Exception('brt', 'Cannot classify if the tree is not rooted')

  if not p.flags.isRegular:
    raise Exception('brt', 'Cannot classify if the graph is not regular')

  if not p.rootAllowAll or not p.leafAllowAll:
    raise Exception('brt', 'Leaves and roots must allow all configurations')

  activeDegree = len(p.activeConstraints[0]) if len(p.activeConstraints) else 3
  passiveDegree = len(p.passiveConstraints[0]) if len(p.passiveConstraints) else 2

  if activeDegree != 3:
    raise Exception('brt', 'Active configurations must be of size 3')

  if passiveDegree != 2:
    raise Exception('brt', 'Passive configurations must be of size 2')

  if not eachConstrIsHomogeneous(p.passiveConstraints):
    raise Exception('brt', 'Passive constraints must be simple pairs of the same labels.')

  alphabet = p.getAlphabet()
  constraints = [moveRootLabelToCenter(x) for x in p.activeConstraints]

  for i, label in enumerate(alphabet):
    constraints = [x.replace(label, str(i+1)) for x in constraints]
  
  result = getProblem(constraints)

  return GenericResponse(
    p,
    complexityMapping[result['upper-bound']],
    complexityMapping[result['lower-bound']],
    UNSOLVABLE,
    complexityMapping[result['lower-bound']], # because randomised LB is also a deterministic LB
    result['solvable-count'],
    result['unsolvable-count']
  )

