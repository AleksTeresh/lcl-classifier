from tqdm import tqdm
from db import updateClassifications
from classifier import classify

def batchClassify(problems):
  return [classify(x) for x in tqdm(problems)]

def classifyAndStore(filename, problems):
  results = batchClassify(problems)
  updateClassifications(results)


