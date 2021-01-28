from problem import GenericProblem
from response import GenericResponse
from complexity import complexities
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

def classify(problem: GenericProblem):
  try:
    cpResult = cpClassify(problem)
  except:
    print('cp-exception')
    cpResult = GenericResponse(problem)

  try:  
    rtResult = rtClassify(problem)
  except:
    print('rt-exception')
    rtResult = GenericResponse(problem)

  try:  
    tlpResult = tlpClassify(problem)
  except:
    print('tlp-exception')
    tlpResult = GenericResponse(problem)

  try:  
    brtResult = brtClassify(problem)
  except:
    print('brt-exception')
    brtResult = GenericResponse(problem)

  responses = [cpResult, rtResult, tlpResult, brtResult]

  return GenericResponse(
    problem,
    getUpperBound(responses, 'randUpperBound'),
    getLowerBound(responses, 'randLowerBound'),
    getUpperBound(responses, 'detUpperBound'),
    getLowerBound(responses, 'detLowerBound'),
    cpResult.solvableCount,
    cpResult.unsolvableCount,
  )
