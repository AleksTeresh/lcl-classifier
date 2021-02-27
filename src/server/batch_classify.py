from typing import List
from tqdm import tqdm
from collections import namedtuple
from db import updateClassifications
from classifier import classify
from bindings.tlp_binding import batchClassify as tlpBatchClassify
from bindings.brt_binding import batchClassify as brtBatchClassify
from problem import GenericProblem, ProblemFlags, ProblemProps
from classified_problem import ClassifiedProblem
from classify_context import ClassifyContext

def batchClassify(problems: List[GenericProblem]):
  context = ClassifyContext()

  try:
    #raise Exception('asasa')
    tlpResponses = tlpBatchClassify(problems)
    context.tlpPreclassified = True
  except Exception as e:
    print(e)
    tlpResponses = []
  except e:
    print(e)

  try:
    brtResponses = brtBatchClassify(problems)
    context.brtPreclassified = True
  except Exception as e:
    print(e)
    brtResponses = []
  except e:
    print(e)
  
  return [
    classify(
      x,
      [x for x in [
        brtResponses[i] if context.brtPreclassified else None,
        tlpResponses[i] if context.tlpPreclassified else None
      ] if x is not None],
      context
    ) for i, x in enumerate(tqdm(problems))
  ]

def classifyAndStore(problems: List[GenericProblem], props: ProblemProps):
  results = batchClassify(problems)
  updateClassifications(results, props)

def batchReclassify(classifiedProblems):
  return [classify(x.toProblem(), x.toResponse()) for x in tqdm(classifiedProblems)]

def reclassifyAndStore(classifiedProblemsDicts):
  objs = [
    ClassifiedProblem(**x) for x in classifiedProblemsDicts
  ]
  
  results = batchReclassify(objs)
  updateClassifications(results)
