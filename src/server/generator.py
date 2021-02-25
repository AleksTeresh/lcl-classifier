from tqdm import tqdm
from util import letterRange, powerset, flatten
from problem import GenericProblem as P, BasicProblemFlags, ProblemProps
from classifier import classify
from complexity import *
from itertools import combinations_with_replacement, product
from storeJson import storeJson

def problemFromConstraints(
  tulpes,
  flags
):
  problems = set()
  for i, (a, b) in enumerate(tqdm(tulpes)):
    if a and b:
      try:
        p = P(
          (
            a if
            (not flags.isDirectedOrRooted) else
            [c.replace(' ', ' : ', 1) for c in a]
          ),
          (
            b if
            (not flags.isDirectedOrRooted) else
            [c.replace(' ', ' : ', 1) for c in b]
          ),
          flags=BasicProblemFlags(
            isTree = flags.isTree,
            isCycle = flags.isCycle,
            isPath = flags.isPath
          ),
          id=i
        )
      except Exception as e:
        if e.args[0] == 'problem':
          continue
        else:
          raise e
      # p.normalize()
      problems.add(p)

  return problems

def generate(
  activeDegree,
  passiveDegree,
  labelCount,
  activesAllSame,
  passivesAllSame,
  flags
):
  alphabet = letterRange(labelCount)
  # take activeDegree labels
  # from a pallete of activeLabelCount
  if flags.isDirectedOrRooted:
    # rooted/directed: order of configs does not matter,
    # except for the frist label in each config. Thus,
    # we have additional product() call below.
    # e.g. degree = 3, labels = 2, gives us:
    # ['AAA', 'AAB', 'ABB', 'BAA', 'BAB', 'BBB']
    actives = ["".join(x) for x in combinations_with_replacement(alphabet, activeDegree-1)]
    passives = ["".join(x) for x in combinations_with_replacement(alphabet, passiveDegree-1)]
    actives = ["".join(x) for x in product(alphabet, actives)]
    passives = ["".join(x) for x in product(alphabet, passives)]
  else:
    # unrooted/undirected: order of configs does not matter
    # e.g. degree 3, labels = 2, gives us
    # ['AAA', 'AAB', 'ABB', 'BBB']
    actives = ["".join(x) for x in combinations_with_replacement(alphabet, activeDegree)]
    passives = ["".join(x) for x in combinations_with_replacement(alphabet, passiveDegree)]

  if activesAllSame:
    actives = [x for x in actives if x[0]*len(x) == x]
  if passivesAllSame:
    passives = [x for x in passives if x[0]*len(x) == x]

  activeConstraints = [tuple([" ".join(y) for y in x]) for x in powerset(actives)]
  passiveConstraints = [tuple([" ".join(y) for y in x]) for x in powerset(passives)]
  problemTuples = set([(a,b) for a in activeConstraints for b in passiveConstraints])
  problemTuples = sorted(list(problemTuples))
  problems = problemFromConstraints(problemTuples, flags)
  return sorted(list(problems), key=lambda p: p.id)
