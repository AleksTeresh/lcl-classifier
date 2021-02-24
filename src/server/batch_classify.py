from typing import List
from tqdm import tqdm
from collections import namedtuple
from db import updateClassifications
from classifier import classify
from problem import GenericProblem, ProblemFlags
from classified_problem import ClassifiedProblem

def batchClassify(problems: List[GenericProblem]):
  return [classify(x) for x in tqdm(problems)]

def classifyAndStore(problems: List[GenericProblem]):
  results = batchClassify(problems)
  updateClassifications(results)

def batchReclassify(classifiedProblems):
  return [classify(x.toProblem(), x.toResponse()) for x in tqdm(classifiedProblems)]

def reclassifyAndStore(classifiedProblemsDicts):
  objs = [
    ClassifiedProblem(**x) for x in classifiedProblemsDicts
  ]
  print(objs[0])
  
  results = batchReclassify(objs)
  updateClassifications(results)
