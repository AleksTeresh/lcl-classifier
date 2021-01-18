import numpy
from file_help import import_data_set
from problem import Problem,alpha_to_problem
from complexity import Complexity
from timeit import default_timer as timer
from input import LOGARITHMIC_LOWER_BOUND
from problem_set import Problem_set

# Get the complexity of a problem
def get_problem(white_constraint,black_constraint, problems):
    problem = alpha_to_problem(white_constraint,black_constraint)
    if problem is None:
        print("error : The problem was incorrectly entered (empty configuration set)")
        return
    for elem in problems:
        if problem == elem:
            return elem
    print("error : The problem was incorrectly entered (wrong degree or more than 3 labels)")

# Get the relaxations of a given problem
def get_relaxations_of(alpha_problem,problems,relaxations,restrictions):
    return relaxations[get_problem(alpha_problem,problems)]

# Get the restrictions of a given problem
def get_restrictions_of(alpha_problem,problems,relaxations,restrictions):
    return restrictions[get_problem(alpha_problem,problems)]

# Get the set of unclassified problems
def get_unclassified_problems(problems,relaxations,restrictions):
    return {x for x in problems if x.get_complexity() == Complexity.Unclassified}

# Get the set of problems with a given complexity
def get_problems_of_complexity(complexity,problems,relaxations,restrictions):
    return {problem for problem in problems if problem.get_complexity()==complexity}

# Return the set of constant problems that have the given upper bound
def get_constant_problems_with_x_rounds_UB(x,problems):
    return {problem for problem in problems if problem.get_complexity()==Complexity.Constant and problem.constant_upper_bound == x}

#Get all the unclassfied problem that does'nt have any unclassified relaxations
def get_UC_problems_with_C_relaxations(problems, relaxations, restrictions):
    return {problem for problem in problems if problem.get_complexity() == Complexity.Unclassified and all([x.get_complexity() != Complexity.Unclassified for x in relaxations[problem]])}

#Get all the unclassfied problem that does'nt have any unclassified restrictions
def get_UC_with_C_restrictions(problems, relaxations, restrictions):
    return {problem for problem in problems if problem.get_complexity() == Complexity.Unclassified and all([x.get_complexity() != Complexity.Unclassified for x in restrictions[problem]])}

#Get the distribution of the upper bounds on constant problems
def get_upper_bounds_constant_problems(problems):
    res = dict()
    for problem in problems:
        if problem.get_complexity()==Complexity.Constant:
            ub = problem.constant_upper_bound
            res[ub] = res.get(ub,0) + 1
    return res

WHITE_DEGREE = 3
BLACK_DEGREE = 2

problems,relaxations,restrictions = import_data_set(WHITE_DEGREE, BLACK_DEGREE,Problem_set.Classified)
black_constraint = {'BC','AA'}
white_constraint = {'AAC', 'BBB'}

print(get_problem(black_constraint,white_constraint,problems))

#print(get_upper_bounds_constant_problems(problems))

#for elem in get_constant_problems_with_x_rounds_UB(9,problems):
#    print(elem)
