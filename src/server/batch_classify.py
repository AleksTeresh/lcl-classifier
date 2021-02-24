from typing import List
from tqdm import tqdm
from db import updateClassifications
from classifier import classify
from problem import GenericProblem

def batchClassify(problems: List[GenericProblem]):
  return [classify(x) for x in tqdm(problems)]

def classifyAndStore(problems: List[GenericProblem]):
  results = batchClassify(problems)
  updateClassifications(results)

def batchReclassify(classifiedProblems):
  return [classify(x, x) for x in tqdm(classifiedProblems)]

def reclassifyAndStore(classifiedProblems):
  results = batchClassify(classifiedProblems)
