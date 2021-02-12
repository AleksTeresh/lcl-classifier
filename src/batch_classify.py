from tqdm import tqdm
from storeJson import storeJson
from classifier import classify

def batchClassify(problems):
  return [classify(x) for x in tqdm(problems)]

def classifyAndStore(filename, problems):
  results = batchClassify(problems)
  storeJson(filename, results)


