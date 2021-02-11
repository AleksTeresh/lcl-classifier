from problem import GenericProblem
from response import GenericResponse
from complexity import complexities
from complexity import *
from bindings.cp_binding import classify as cpClassify
from bindings.rt_binding import classify as rtClassify
from bindings.tlp_binding import classify as tlpClassify
from bindings.brt_binding import classify as brtClassify

def getUpperBound(responses, attrStr):
  return complexities[
    min([complexities.index(getattr(res, attrStr)) for res in responses])
  ]

def getLowerBound(responses, attrStr):
  return complexities[
    max([complexities.index(getattr(res, attrStr)) for res in responses])
  ]

def removeUnknowns(response):
  if response.randLowerBound == UNKNOWN:
    response.randLowerBound = CONST
  if response.detLowerBound == UNKNOWN:
    response.detLowerBound = CONST
  if response.randUpperBound == UNKNOWN:
    response.randUpperBound = UNSOLVABLE
  if response.detUpperBound == UNKNOWN:
    response.detUpperBound = UNSOLVABLE
  return response

def propagateBounds(response):
  # print(response.randUpperBound, response.detUpperBound)
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

def postprocess(response):
  response = removeUnknowns(response)
  response = propagateBounds(response)
  return response

def classify(problem: GenericProblem):
  try:
    cpResult = cpClassify(problem)
  except Exception as e:
    cpResult = GenericResponse(problem)
  except e:
    print(e)

  try:  
    rtResult = rtClassify(problem)
  except Exception as e:
    rtResult = GenericResponse(problem)
  except e:
    print(e)

  try:  
    tlpResult = tlpClassify(problem)
  except Exception as e:
    tlpResult = GenericResponse(problem)
  except e:
    print(e)

  try:  
    brtResult = brtClassify(problem)
  except Exception as e:
    brtResult = GenericResponse(problem)
  except e:
    print(e)

  responses = [cpResult, rtResult, tlpResult, brtResult]

  response = GenericResponse(
    problem,
    getUpperBound(responses, 'randUpperBound'),
    getLowerBound(responses, 'randLowerBound'),
    getUpperBound(responses, 'detUpperBound'),
    getLowerBound(responses, 'detLowerBound'),
    cpResult.solvableCount,
    cpResult.unsolvableCount,
  )
  # print(response)
  return postprocess(response)
