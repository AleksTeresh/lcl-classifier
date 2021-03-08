import sys, getopt, pickle
from problem import GenericProblem, ProblemFlags, ProblemProps
from classifier import classify
from batch_classify import batchClassify
from generator import generate
from complexity import *
from statistics import compute as computeStats, prettyPrint
from query import Query, Bounds, QueryExcludeInclude
from batch_classify import classifyAndStore, reclassifyAndStore
from db import storeProblemsAndGetWithIds, getClassifiedProblemObjs, getProblem

activeDegree = 2
passiveDegree = 2
labelCount = 4
activesAllSame = False
passivesAllSame = False
flags = ProblemFlags(
  isTree=False,
  isCycle=False,
  isPath=True,
  isDirectedOrRooted=False
)

props = ProblemProps(
  activeDegree,
  passiveDegree,
  labelCount,
  activesAllSame,
  passivesAllSame,
  flags = flags
)

query = Query(
  props,
  bounds = Bounds(
    # randUpperBound=UNSOLVABLE,
    # randLowerBound=CONST
  ),
  excludeInclude = QueryExcludeInclude(
  #  includeIfConfigHasAllOf = ['A A', 'A B'],
  #  excludeIfConfigHasSomeOf = ['B C', 'B B'],
  #  returnSmallestProblemOnly = True,
  #  returnLargestProblemOnly = True
  )
)

ps = generate(
  activeDegree,
  passiveDegree,
  labelCount,
  activesAllSame,
  passivesAllSame,
  flags,
  countLimit=5000,
  skipCount=20000
)

psWithIds = storeProblemsAndGetWithIds(ps, props)
classifyAndStore(
  psWithIds,
  isCompleteClassification=False,
  props=props
)

# # classifiedProblems = getClassifiedProblemObjs(query)
# # reclassifyAndStore(classifiedProblems)

res = getClassifiedProblemObjs(query)
stats = computeStats(res)
prettyPrint(stats)
