from problem import GenericProblem
from response import GenericResponse
from complexity import complexities
from complexity import *
from classify_context import ClassifyContext
from typing import List, Dict
from bindings.cp_binding import classify as cpClassify
from bindings.rt_binding import classify as rtClassify
from bindings.tlp_binding import classify as tlpClassify
from bindings.brt_binding import classify as brtClassify

def getUpperBound(
  responses: Dict[str, GenericResponse],
  attrStr: str
):
  return complexities[
    min([complexities.index(getattr(res, attrStr)) for res in responses.values()])
  ]

def getLowerBound(
  responses: Dict[str, GenericResponse],
  attrStr: str
):
  return complexities[
    max([complexities.index(getattr(res, attrStr)) for res in responses.values()])
  ]

def removeUnknowns(response: GenericResponse):
  if response.randLowerBound == UNKNOWN:
    response.randLowerBound = CONST
  if response.detLowerBound == UNKNOWN:
    response.detLowerBound = CONST
  if response.randUpperBound == UNKNOWN:
    response.randUpperBound = UNSOLVABLE
  if response.detUpperBound == UNKNOWN:
    response.detUpperBound = UNSOLVABLE
  return response

def propagateBounds(response: GenericResponse):
  # propagate rand upper
  response.randUpperBound = complexities[min(
    complexities.index(response.randUpperBound),
    complexities.index(response.detUpperBound)
  )]
  # propagate det lower
  response.detLowerBound = complexities[max(
    complexities.index(response.randLowerBound),
    complexities.index(response.detLowerBound)
  )]

  # propagate det upper
  if response.randUpperBound != LOGLOG:
    response.detUpperBound = response.randUpperBound
  else:
    response.detUpperBound = complexities[min(
      complexities.index(response.detUpperBound),
      complexities.index(LOG)
    )]
  # propagate rand lower
  if response.detLowerBound != LOG:
    response.randLowerBound = response.detLowerBound
  else:
    response.randLowerBound = complexities[max(
      complexities.index(response.randLowerBound),
      complexities.index(LOGLOG)
    )]
  return response

def postprocess(response: GenericResponse):
  response = removeUnknowns(response)
  response = propagateBounds(response)
  return response

def checkForContradictions(
  responses: Dict[str, GenericResponse]
):
  randUpperBound = getUpperBound(responses, 'randUpperBound')
  detUpperBound = getUpperBound(responses, 'detUpperBound')
  randLowerBound = getLowerBound(responses, 'randLowerBound')
  detLowerBound = getLowerBound(responses, 'detLowerBound')
  for r in responses.values():
    if complexities.index(r.randLowerBound) > complexities.index(randUpperBound):
      raise Exception('classification-contradiction', 'randLowerBound in one of the respones is > randUpperBound in another response', responses, r.problem)
    if complexities.index(r.detLowerBound) > complexities.index(detUpperBound):
      raise Exception('classification-contradiction' 'detLowerBound in one of the respones is > detUpperBound in another response', responses, r.problem)
    if complexities.index(r.randUpperBound) < complexities.index(randLowerBound):
      raise Exception('classification-contradiction' 'randUpperBound in one of the respones is < randLowerBound in another response', responses, r.problem)
    if complexities.index(r.detUpperBound) < complexities.index(detLowerBound):
      raise Exception('classification-contradiction' 'randUpperBound in one of the respones is < randLowerBound in another response', responses, r.problem)


def classify(
  problem: GenericProblem,
  existingClassifications: Dict[str, GenericResponse] = {},
  context: ClassifyContext = ClassifyContext()
):
  try:
    cpResult = cpClassify(problem, context)
  except Exception as e:
    cpResult = GenericResponse(problem)
  except e:
    print(e)

  try:  
    rtResult = rtClassify(problem, context)
  except Exception as e:
    rtResult = GenericResponse(problem)
  except e:
    print(e)

  try:  
    tlpResult = tlpClassify(problem, context)
  except Exception as e:
    tlpResult = GenericResponse(problem)
  except e:
    print(e)

  try:  
    brtResult = brtClassify(problem, context)
  except Exception as e:
    brtResult = GenericResponse(problem)
  except e:
    print(e)

  responses = {
    'cp': cpResult,
    'rt': rtResult,
    'tlp': tlpResult,
    'brt': brtResult,
    **existingClassifications
  }

  checkForContradictions(responses)

  response = GenericResponse(
    problem,
    getUpperBound(responses, 'randUpperBound'),
    getLowerBound(responses, 'randLowerBound'),
    getUpperBound(responses, 'detUpperBound'),
    getLowerBound(responses, 'detLowerBound'),
    cpResult.solvableCount,
    cpResult.unsolvableCount,
  )

  return postprocess(response)
