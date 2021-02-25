from problem import GenericProblem
from parser import parseConfigs
from config_util import normalizeConstraints

def tryUpperBound(problem):
  iter_label = [(20,3),(8,4),(9,4)]
  for pair in iter_label:
    ub = round_eliminator_ub(problem, pair[0], pair[1])
    if ub >= 0:
      problem.set_complexity(Complexity.Constant)
      problem.constant_upper_bound = min(problem.constant_upper_bound,ub)

def tryLowerBound(problem):
  iter_label = [(15,5)]
  for pair in iter_label:
    lb = round_eliminator_lb(problem, pair[0], pair[1])
    if lb >= 0:
      problem.set_complexity(Complexity.Constant)
      problem.constant_lower_bound = max(problem.constant_lower_bound,lb)

def tryConstantComplexity(problem):
  tryLowerBound(problem)
  tryUpperBound(problem)

def classifyByRE(problem: GenericProblem):
  if problem.flags.isCycle:
    raise Exception('tlp', 'Cannot classify if the graph is a cycle')

  if problem.flags.isDirectedOrRooted:
    raise Exception('tlp', 'Cannot classify if the tree is rooted')

  if not problem.flags.isRegular:
    raise Exception('tlp', 'Cannot classify if the graph is not regular')

  if not problem.rootAllowAll or not problem.leafAllowAll:
    raise Exception('tlp', 'Leaves and roots must allow all configurations')

  parsedActives = parseConfigs(problem.activeConstraints)
  parsedPassives = parseConfigs(problem.passiveConstraints)

  activeConstraints = list(normalizeConstraints(parsedActives))
  passiveConstraints = list(normalizeConstraints(parsedPassives))

  problem = alpha_to_problem(activeConstraints, passiveConstraints)
  tryConstantComplexity(problem)
  print(problem)
  print(problem.constant_lower_bound)
  print(problem.constant_upper_bound)
  
