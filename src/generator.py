from tqdm import tqdm
from util import letterRange, powerset, flatten
from problem import GenericProblem as P, ProblemFlags
from classifier import classify
from complexity import *
from itertools import combinations_with_replacement, product
from storeJson import storeJson
from batch_classify import classifyAndStore

def problemFromConstraints(
  tulpes,
  flags
):
  problems = set()
  for i, (a, b) in enumerate(tqdm(tulpes)):
    if a and b:
      try:
        p = P(
          a,
          b,
          flags=flags,
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
  if flags.isRooted:
    actives = ["".join(x) for x in combinations_with_replacement(alphabet, activeDegree-1)]
    passives = ["".join(x) for x in combinations_with_replacement(alphabet, passiveDegree-1)]
    actives = ["".join(x) for x in product(alphabet, actives)]
    passives = ["".join(x) for x in product(alphabet, passives)]
  else:
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

fileNameSuffix = (f'_rooted_bin_{activeDegree}_{passiveDegree}_{labelCount}_' +
  ('t_' if activesAllSame else 'f_') +
  ('t_' if passivesAllSame else 'f_') +
  ('t' if flags.isRooted else 'f') +
  '.json')
storeJson('problems' + fileNameSuffix, ps)
classifyAndStore('results' + fileNameSuffix, ps)

# tlpProblem1 = P(
#   ['A B', 'C C', 'D ADC'],
#   ['B B C', 'A A A', 'B B B', 'A A C', 'B C C', 'Y X B'],
#   id=1
# )
# tlpProblem1.normalize()

# tlpProblem2 = P(
#   ['A C', 'B B'],
#   ['C C B', 'A A A', 'C C C', 'A A B', 'C B B'],
#   id=2
# )
# tlpProblem2.normalize()

# tlpProblem3 = P(
#   ['A C', 'B B'],
#   ['C C B', 'A A A', 'C C C', 'A A B', 'C B B'],
#   id=3
# )
# tlpProblem3.normalize()

# ps = set()

# ps.add(tlpProblem1)
# ps.add(tlpProblem2)
# ps.add(tlpProblem3)
