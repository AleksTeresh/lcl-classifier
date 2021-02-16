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

def prettyPrint(stats):
  print("In total: %s problems" % stats.totalSize)
  print()

  print('Stats for randomised setting:')
  print('*****************************')
  print()
  print("Solvable in constant time: %s " % stats.const.randSolvable)
  print("Solvable in log* time: %s " % stats.logStar.randSolvable)
  print("Solvable in loglog time: %s " % stats.logLog.randSolvable)
  print("Solvable in log time: %s " % stats.log.randSolvable)
  print("Solvable in linear time: %s " % stats.linear.randSolvable)
  print("Unsolvable: %s" % stats.unsolvable.randSolvable)
  print("TBD: %s" % (
    stats.totalSize -
    stats.const.randSolvable -
    stats.logStar.randSolvable -
    stats.logLog.randSolvable -
    stats.log.randSolvable -
    stats.linear.randSolvable -
    stats.unsolvable.randSolvable
  ))
  print()

  print('Lower bounds:')
  print("Constant time: %s " % stats.const.randLowerBound)
  print("Log* time: %s " % stats.logStar.randLowerBound)
  print("Loglog time: %s " % stats.logLog.randLowerBound)
  print("Log time: %s " % stats.log.randLowerBound)
  print("Linear time: %s " % stats.linear.randLowerBound)
  print("Unsolvable: %s" % stats.unsolvable.randLowerBound)
  print("TBD: %s" % (
    stats.totalSize -
    stats.const.randLowerBound -
    stats.logStar.randLowerBound -
    stats.logLog.randLowerBound -
    stats.log.randLowerBound -
    stats.linear.randLowerBound -
    stats.unsolvable.randLowerBound
  ))
  print()

  print('Upper bounds:')
  print("Constant time: %s " % stats.const.randUpperBound)
  print("Log* time: %s " % stats.logStar.randUpperBound)
  print("Loglog time: %s " % stats.logLog.randUpperBound)
  print("Log time: %s " % stats.log.randUpperBound)
  print("Linear time: %s " % stats.linear.randUpperBound)
  print("Unsolvable: %s" % stats.unsolvable.randUpperBound)
  print("TBD: %s" % (
    stats.totalSize -
    stats.const.randUpperBound -
    stats.logStar.randUpperBound -
    stats.logLog.randUpperBound -
    stats.log.randUpperBound -
    stats.linear.randUpperBound -
    stats.unsolvable.randUpperBound
  ))
  print()

  print('Stats for deterministic setting:')
  print('*****************************')
  print()
  print("Solvable in constant time: %s " % stats.const.detSolvable)
  print("Solvable in log* time: %s " % stats.logStar.detSolvable)
  print("Solvable in loglog time: %s " % stats.logLog.detSolvable)
  print("Solvable in log time: %s " % stats.log.detSolvable)
  print("Solvable in linear time: %s " % stats.linear.detSolvable)
  print("Unsolvable: %s" % stats.unsolvable.detSolvable)
  print("TBD: %s" % (
    stats.totalSize -
    stats.const.detSolvable -
    stats.logStar.detSolvable -
    stats.logLog.detSolvable -
    stats.log.detSolvable -
    stats.linear.detSolvable -
    stats.unsolvable.detSolvable
  ))
  print()

  print('Lower bounds:')
  print("Constant time: %s " % stats.const.detLowerBound)
  print("Log* time: %s " % stats.logStar.detLowerBound)
  print("Loglog time: %s " % stats.logLog.detLowerBound)
  print("Log time: %s " % stats.log.detLowerBound)
  print("Linear time: %s " % stats.linear.detLowerBound)
  print("Unsolvable: %s" % stats.unsolvable.detLowerBound)
  print("TBD: %s" % (
    stats.totalSize -
    stats.const.detLowerBound -
    stats.logStar.detLowerBound -
    stats.logLog.detLowerBound -
    stats.log.detLowerBound -
    stats.linear.detLowerBound -
    stats.unsolvable.detLowerBound
  ))
  print()

  print('Upper bounds:')
  print("Constant time: %s " % stats.const.detUpperBound)
  print("Log* time: %s " % stats.logStar.detUpperBound)
  print("Loglog time: %s " % stats.logLog.detUpperBound)
  print("Log time: %s " % stats.log.detUpperBound)
  print("Linear time: %s " % stats.linear.detUpperBound)
  print("Unsolvable: %s" % stats.unsolvable.detUpperBound)
  print("TBD: %s" % (
    stats.totalSize -
    stats.const.detUpperBound -
    stats.logStar.detUpperBound -
    stats.logLog.detUpperBound -
    stats.log.detUpperBound -
    stats.linear.detUpperBound -
    stats.unsolvable.detUpperBound
  ))
  print()

def printStatistics(filePath):
    stats = compute(filePath)
    prettyPrint(stats)

printStatistics('./problems/results_rooted_bin_3_2_2_f_t_t.json')
