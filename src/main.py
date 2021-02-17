import sys, getopt
from problem import GenericProblem, ProblemFlags, ProblemProps
from classifier import classify
from generator import generate
from complexity import *
from statistics import compute as computeStats, prettyPrint
from query import Query, Bounds, QueryExcludeInclude
from batch_classify import classifyAndStore
from db import storeProblemsAndGetWithIds, getProblems

# REtorProblem1 = GenericProblem(
#   activeConstraints = ['M U U U', 'P P P P'],
#   passiveConstraints = ['M UP UP UP', 'U U U U']
# )

# REtorProblem2 = GenericProblem(
#   activeConstraints = ['M(W->B) S(W->B)(B->W)MP (W->B)(B->W) (W->B)(B->W)SUS'],
#   passiveConstraints = ['(B->W) (W->B)(B->W) (W->B)(B->W)']
# )

# # const, 1 round solvable
# REtorProblem3 = GenericProblem(
#   ['M U U U', 'PM PM PM PM'],
#   ['M UP UP UP', 'U U U U']
# )

activeDegree = 3
passiveDegree = 2
labelCount = 2
activesAllSame = False
passivesAllSame = True
flags = ProblemFlags(
  isTree=True,
  isCycle=False,
  isPath=False,
  isDirected=False,
  isRooted=True,
  isRegular=True
)

ps = generate(
  activeDegree,
  passiveDegree,
  labelCount,
  activesAllSame,
  passivesAllSame,
  flags
)

props = ProblemProps(
  activeDegree,
  passiveDegree,
  labelCount,
  activesAllSame,
  passivesAllSame,
  flags
)

psWithIds = storeProblemsAndGetWithIds(ps, props)
classifyAndStore(ps)

query = Query(
  props,
  bounds = Bounds(
    randUpperBound=LOG,
    randLowerBound=ITERATED_LOG
  )
)

res = getProblems(query)
stats = computeStats(res)
prettyPrint(stats)
