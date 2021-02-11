from tqdm import tqdm
from util import letterRange, powerset, flatten
from problem import GenericProblem as P
from classifier import classify
from complexity import *
from itertools import combinations_with_replacement, product
import os, json

def problemFromConstraints(tulpes):
  problems = set()
  for (a, b) in tqdm(tulpes):
    if a and b:
      try:
        p = P(a,b, isTree=True, isCycle=False, isPath=False, isRooted=True, isRegular=True)
      except Exception as e:
        if e.args[0] == 'problem':
          continue
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
  labelCount,
  activesAllSame = False,
  passivesAllSame = False,
  rooted = False
):
  alphabet = letterRange(labelCount)
  # take activeDegree labels
  # from a pallete of activeLabelCount
  if rooted:
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
  problems = problemFromConstraints(problemTuples)
  return problems

# p = P(
#   ['2 1 1', '1 1 2'],
#   ['1 1', '2 2'],
#   isTree=True, isCycle=False, isPath=False, isRooted=True, isRegular=True)
# p.normalize()
# print(p.activeConstraints, p.passiveConstraints)
ps = generate(3, 2, 3, passivesAllSame=True, rooted=True)

with open(os.path.dirname(os.path.realpath(__file__)) + '/problems/problems-temp.json', 'w+', encoding='utf-8') as f:
  json.dump(ps, f, ensure_ascii=False, indent=2)

tightCtr = 0
constCtr = 0
logStartCtr = 0
logCtr = 0
globalCtr = 0
unsolvableCtr = 0
for p in ps:
  res = classify(p)
  if res.randUpperBound == res.randLowerBound:
    tightCtr += 1
    if res.randUpperBound == CONST:
      constCtr += 1
    if res.randUpperBound == ITERATED_LOG:
      logStartCtr += 1
    if res.randUpperBound == LOG:
      logCtr += 1
    if res.randUpperBound == GLOBAL:
      globalCtr += 1
    if res.randUpperBound == UNSOLVABLE:
      unsolvableCtr += 1

print("Total: ", len(ps))
print("Tight: ", tightCtr)
print("(1): ", constCtr)
print("(log* n): ", logStartCtr)
print("(log n): ", logCtr)
print("(n): ", globalCtr)
print(" - : ", unsolvableCtr)
