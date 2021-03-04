from problem import GenericProblem
from response import GenericResponse, Sources
from complexity import complexities
from complexity import *
from classifier_types import *
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
  classifierToComplexityIdx = {
    k: complexities.index(getattr(res, attrStr)) for k, res in responses.items()
  }
  minClassifier = min(
    classifierToComplexityIdx,
    key=classifierToComplexityIdx.get
  )
  minComplexityIdx = classifierToComplexityIdx[minClassifier]
  return minClassifier, complexities[minComplexityIdx]

def getLowerBound(
  responses: Dict[str, GenericResponse],
  attrStr: str
):
  classifierToComplexityIdx = {
    k: complexities.index(getattr(res, attrStr)) for k, res in responses.items()
  }
  maxClassifier = max(
    classifierToComplexityIdx,
    key=classifierToComplexityIdx.get
  )
  maxComplexityIdx = classifierToComplexityIdx[maxClassifier]
  return maxClassifier, complexities[maxComplexityIdx]

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
  if (
    complexities.index(response.detUpperBound) <
    complexities.index(response.randUpperBound)
  ):
    response.randUpperBound = response.detUpperBound
    response.papers.randUpperBoundSource = response.papers.detUpperBoundSource

  # propagate det lower
  if (
    complexities.index(response.randLowerBound) >
    complexities.index(response.detLowerBound)
  ):
    response.detLowerBound = response.randLowerBound
    response.papers.detLowerBoundSource = response.papers.randLowerBoundSource

  # propagate det upper
  if response.randUpperBound != LOGLOG:
    response.detUpperBound = response.randUpperBound
    response.papers.detUpperBoundSource = response.papers.randUpperBoundSource
  else:
    response.detUpperBound = complexities[min(
      complexities.index(response.detUpperBound),
      complexities.index(LOG)
    )]
  # propagate rand lower
  if response.detLowerBound != LOG:
    response.randLowerBound = response.detLowerBound
    response.papers.randLowerBoundSource = response.papers.detLowerBoundSource
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
  _, randUpperBound = getUpperBound(responses, 'randUpperBound')
  _, detUpperBound = getUpperBound(responses, 'detUpperBound')
  _, randLowerBound = getLowerBound(responses, 'randLowerBound')
  _, detLowerBound = getLowerBound(responses, 'detLowerBound')
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
    Classifier.CP: cpResult,
    Classifier.RT: rtResult,
    Classifier.TLP: tlpResult,
    Classifier.BRT: brtResult,
    **existingClassifications
  }

  checkForContradictions(responses)

  rubSource, rub = getUpperBound(responses, 'randUpperBound')
  rlbSource, rlb = getLowerBound(responses, 'randLowerBound')
  dubSource, dub = getUpperBound(responses, 'detUpperBound')
  dlbSource, dlb = getLowerBound(responses, 'detLowerBound')

  response = GenericResponse(
    problem,
    rub,
    rlb,
    dub,
    dlb,
    cpResult.solvableCount,
    cpResult.unsolvableCount,
    papers = Sources(
      context.sources[rubSource],
      context.sources[rlbSource],
      context.sources[dubSource],
      context.sources[dlbSource]
    )
  )

  return postprocess(response)
