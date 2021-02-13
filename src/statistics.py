from complexity import *
import json
from tqdm import tqdm
from typing import NamedTuple

class ComplexityClassData():
  def __init__(
    self,
    randLowerBound: int = 0,
    detLowerBound: int = 0,
    randUpperBound: int = 0,
    detUpperBound: int = 0,  
    randSolvable: int = 0,
    detSolvable: int = 0
  ):
    self.randLowerBound = randLowerBound
    self.detLowerBound = detLowerBound
    self.randUpperBound = randUpperBound
    self.detUpperBound = detUpperBound
    
    self.randSolvable = randSolvable
    self.detSolvable = detSolvable

class StatisticsData():
  def __init__(self):
    self.const: ComplexityClassData = ComplexityClassData()
    self.logStar: ComplexityClassData = ComplexityClassData()
    self.logLog: ComplexityClassData = ComplexityClassData()
    self.log: ComplexityClassData = ComplexityClassData()
    self.linear: ComplexityClassData = ComplexityClassData()
    self.unsolvable: ComplexityClassData = ComplexityClassData()
    self.totalSize: int = 0

def compute(filePath):
  with open(filePath) as json_file:
    data = json.load(json_file)
    stats = StatisticsData()
    complexityMap = {
      CONST: 'const',
      ITERATED_LOG: 'logStar',
      LOGLOG: 'logLog',
      LOG: 'log',
      GLOBAL: 'linear',
      UNSOLVABLE: 'unsolvable',
    }

    for p in tqdm(data):
      randLowerBound = p["randUpperBound"]
      randUpperBound = p["randLowerBound"]
      detLowerBound = p["detUpperBound"]
      detUpperBound = p["detLowerBound"]

      cl = complexityMap[randLowerBound]
      cu = complexityMap[randUpperBound]
      getattr(stats, cl).randLowerBound += 1
      getattr(stats, cu).randUpperBound += 1
      if cl == cu:
        getattr(stats, cu).randSolvable += 1  
    
      cl = complexityMap[detLowerBound]
      cu = complexityMap[detUpperBound]       
      getattr(stats, cl).detLowerBound += 1      
      getattr(stats, cu).detUpperBound += 1
      if cl == cu:
        getattr(stats, cu).detSolvable += 1  

    stats.totalSize = len(data)
    return stats

def printStats(stats):
  print("In total: %s problems" % stats.totalSize)
  # TODO: pretty printing


  # print("Solvable in constant time: %s " % constSolvable)
  # print("Solvable in log* time: %s " % logStarSolvable)
  # print("Solvable in loglog time: %s " % loglogSolvable)
  # print("Solvable in log time: %s " % logSolvable)
  # print("Solvable in linear time: %s " % linearSolvable)
  # print("Unsolvable: %s" % unsolvable)
  # print("TBD: %s" % (totalSize - unsolvable - constSolvable - logStarSolvable - loglogSolvable - logSolvable - linearSolvable))
  # print()

  # print("Lower bounds")
  # print("Constant time: %s " % lowerBoundConstant)
  # print("Log* time: %s " % lowerBoundLogStar)
  # print("Loglog time: %s " % lowerBoundLoglog)
  # print("Log time: %s " % lowerBoundLog)
  # print("Linear time: %s " % lowerBoundLinear)
  # print("TBD: %s" % (totalSize - unsolvable - lowerBoundConstant - lowerBoundLogStar - lowerBoundLoglog - lowerBoundLog - lowerBoundLinear))
  # print()

  # print("Upper bounds")
  # print("Constant time: %s " % upperBoundConstant)
  # print("Log* time: %s " % upperBoundLogStar)
  # print("Loglog time: %s " % upperBoundLoglog)
  # print("Log time: %s " % upperBoundLog)
  # print("Linear time: %s " % upperBoundLinear)
  # print("TBD: %s" % (totalSize - unsolvable - upperBoundConstant - upperBoundLogStar - upperBoundLoglog - upperBoundLog - upperBoundLinear))

def printStatistics(filePath):
    stats = compute(filePath)
    printStats(stats)

printStatistics('./problems/results_rooted_bin_3_2_2.json')



  

# tightCtr = 0
# constCtr = 0
# logStartCtr = 0
# logCtr = 0
# globalCtr = 0
# unsolvableCtr = 0
# classified = []
# for p in tqdm(ps):
#   res = classify(p)
#   classified.append(res)
#   if res.randUpperBound == res.randLowerBound:
#     tightCtr += 1
#     if res.randUpperBound == CONST:
#       constCtr += 1
#     if res.randUpperBound == ITERATED_LOG:
#       logStartCtr += 1
#     if res.randUpperBound == LOG:
#       logCtr += 1
#     if res.randUpperBound == GLOBAL:
#       globalCtr += 1
#     if res.randUpperBound == UNSOLVABLE:
#       unsolvableCtr += 1

# with open(os.path.dirname(os.path.realpath(__file__)) + '/problems/classified.json', 'w+', encoding='utf-8') as f:
#   json.dump([x.__dict__ for x in classified], f, ensure_ascii=False, indent=2)

# print("Total: ", len(ps))
# print("Tight: ", tightCtr)
# print("(1): ", constCtr)
# print("(log* n): ", logStartCtr)
# print("(log n): ", logCtr)
# print("(n): ", globalCtr)
# print(" - : ", unsolvableCtr)
