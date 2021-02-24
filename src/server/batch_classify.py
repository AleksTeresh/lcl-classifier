from typing import List
from tqdm import tqdm
from collections import namedtuple
from db import updateClassifications
from classifier import classify
from problem import GenericProblem, ProblemFlags

def batchClassify(problems: List[GenericProblem]):
  return [classify(x) for x in tqdm(problems)]

def classifyAndStore(problems: List[GenericProblem]):
  results = batchClassify(problems)
  updateClassifications(results)

# def batchReclassify(classifiedProblems):
#   return [classify(x, x) for x in tqdm(classifiedProblems)]

# def reclassifyAndStore(classifiedProblems):
#   objs = []
#   for p in classifiedProblems:
#     obj = namedtuple("ClassifiedProblem", [*p.keys(), 'flags'])(*p.values(), ProblemFlags(
#       isTree=p['isTree'],
#       isCycle=p['isCycle'],
#       isPath=p['isPath'],
#       isDirected=p['isDirected'],
#       isRooted=p['isRooted'],
#       isRegular=p['isRegular'],
#     ))
#     # obj.flags = 
#     objs.append(obj)
  
#   results = batchReclassify(objs)
#   updateClassifications(results)
