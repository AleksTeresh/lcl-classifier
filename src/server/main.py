import sys, getopt
from problem import GenericProblem, ProblemFlags, ProblemProps
from classifier import classify
from generator import generate
from complexity import *
from statistics import compute as computeStats, prettyPrint
from query import Query, Bounds, QueryExcludeInclude
from batch_classify import classifyAndStore
from db import storeProblemsAndGetWithIds, getProblems, getProblem

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

activeDegree = 2
passiveDegree = 2
labelCount = 3
activesAllSame = False
passivesAllSame = False
flags = ProblemFlags(
  isTree=False,
  isCycle=False,
  isPath=True,
  isDirected=False,
  isRooted=False
)

# ps = generate(
#   activeDegree,
#   passiveDegree,
#   labelCount,
#   activesAllSame,
#   passivesAllSame,
#   flags
# )

props = ProblemProps(
  activeDegree,
  passiveDegree,
  labelCount,
  activesAllSame,
  passivesAllSame,
  flags
)

# psWithIds = storeProblemsAndGetWithIds(ps, props)
# classifyAndStore(ps)

query = Query(
  props,
  bounds = Bounds(
    randUpperBound=ITERATED_LOG,
    randLowerBound=CONST
  ),
 excludeInclude = QueryExcludeInclude(
   includeIfConfigHasAllOf = ['A A', 'A B'],
   excludeIfConfigHasSomeOf = ['B C', 'B B'],
   # returnSmallestProblemOnly = True,
   # returnLargestProblemOnly = True
 )
)

res = getProblems(query)
print(res)
stats = computeStats(res)
prettyPrint(stats)

problem = GenericProblem(
  activeConstraints = ['A A', 'A B'],
  passiveConstraints = ['A A', 'A B'],
  flags = ProblemFlags(
    isTree = False,
    isCycle = True,
    isPath = False
  )
)

r = getProblem(problem)
print(r)
