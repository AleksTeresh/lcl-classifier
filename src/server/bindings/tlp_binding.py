from typing import List
from problem import GenericProblem
from classify_context import ClassifyContext
from tlp_classifier import get_problem, get_problems, complexity_name, Complexity as tlpComplexity
from config_util import normalizeConstraints
from response import GenericResponse
from complexity import *

complexityMapping = {
  tlpComplexity.Constant: CONST,
  tlpComplexity.Iterated_Logarithmic: ITERATED_LOG,
  tlpComplexity.Logarithmic: LOG,
  tlpComplexity.Global: GLOBAL,
  tlpComplexity.Unsolvable: UNSOLVABLE,
  tlpComplexity.Unclassified: UNKNOWN
}

def batchClassify(ps: List[GenericProblem]):
  representativeP = ps[0]
  try:
    classify(representativeP)
  except:
    raise Exception('Cannot batch classify')

  results = get_problems(
    [(
      p.activeConstraints,
      p.passiveConstraints
    ) for p in ps]
  )
  return [
    GenericResponse(
      ps[i],
      complexityMapping[r.upper_bound],  # because deterministic UB is also a randomised UB
      CONST,
      complexityMapping[r.upper_bound],
      complexityMapping[r.lower_bound],
    ) for i, r in enumerate(results)
  ]

def classify(
  p: GenericProblem,
  context: ClassifyContext = ClassifyContext()
):
  if context.tlpPreclassified:
    return GenericResponse(p)

  if p.flags.isCycle:
    raise Exception('tlp', 'Cannot classify if the graph is a cycle')

  if p.flags.isRooted:
    raise Exception('tlp', 'Cannot classify if the tree is rooted')

  if p.flags.isDirected:
    raise Exception('tlp', 'Cannot classify if the path is directed')

  if not p.flags.isRegular:
    raise Exception('tlp', 'Cannot classify if the graph is not regular')

  if not p.rootAllowAll or not p.leafAllowAll:
    raise Exception('tlp', 'Leaves and roots must allow all configurations')

  activeDegree = len(p.activeConstraints[0]) if len(p.activeConstraints) else 3
  passiveDegree = len(p.passiveConstraints[0]) if len(p.passiveConstraints) else 2

  if not (
    (activeDegree == 2 and passiveDegree == 2) or
    (activeDegree == 2 and passiveDegree == 3) or
    (activeDegree == 3 and passiveDegree == 2)):
    raise Exception('rooted-tree', 'Allowed degrees pairs are (2, 2), (2, 3), (3, 2)')

  result = get_problem(p.activeConstraints, p.passiveConstraints)

  return GenericResponse(
    p,
    complexityMapping[result.upper_bound],  # because deterministic UB is also a randomised UB
    CONST,
    complexityMapping[result.upper_bound],
    complexityMapping[result.lower_bound],
  )
