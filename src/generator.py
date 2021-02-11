from tqdm import tqdm
from util import letterRange, powerset, flatten
from problem import GenericProblem as P
from itertools import combinations_with_replacement

def problemFromConstraints(tulpes):
  problems = set()
  for (a, b) in tqdm(tulpes):
    if a and b:
      try:
        p = P(a,b)
      except Exception as e:
        if e.args[0] == 'problem':
          pass
        else:
          raise e
      p.normalize()
      problems.add(p)

  for p in problems:
    print(p.activeConstraints, p.passiveConstraints)
  return problems


def generate(
  activeDegree,
  passiveDegree,
  labelCount
):
  alphabet = letterRange(labelCount)
  # take activeDegree labels
  # from a pallete of activeLabelCount
  actives = ["".join(x) for x in combinations_with_replacement(alphabet, activeDegree)]
  passives = ["".join(x) for x in combinations_with_replacement(alphabet, passiveDegree)]
  activeConstraints = [tuple([" ".join(y) for y in x]) for x in powerset(actives)]
  passiveConstraints = [tuple([" ".join(y) for y in x]) for x in powerset(passives)]
  problemTuples = set([(a,b) for a in activeConstraints for b in passiveConstraints])

  problems = problemFromConstraints(problemTuples)
  print(len(problems))

generate(2, 3, 3)
