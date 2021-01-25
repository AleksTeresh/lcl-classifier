import sys, getopt
from problem import GenericProblem, TlpProblem, BinaryRootedTreeProblem
from parser import parseConfigs

REtorProblem1 = GenericProblem(
  activeConstraints = {'M U U U', 'P P P P'},
  passiveConstraints = {'M UP UP UP', 'U U U U'}
)

REtorProblem2 = GenericProblem(
  activeConstraints = {'M(W->B) (W->B)(B->W)MP (W->B)(B->W)'},
  passiveConstraints = {'(B->W) (W->B)(B->W) (W->B)(B->W)'}
)

print(parseConfigs(REtorProblem1.activeConstraints))
print(parseConfigs(REtorProblem2.activeConstraints))
 
# AB CC BC
# AAA AAB AAC BCC ACC
tlpProblem = GenericProblem(
  {'A B', 'C C', 'B C'},
  {'A A A', 'A A B', 'A A C', 'B C C', 'A C C'}
)

# "111",
# "121",
# "131"
# "132"
# decider, tree-classification
binaryRootedTreeProblem = GenericProblem(
  {'A a a', 'B a a', 'C a a', 'C a b'},
  {'A a', 'B b', 'C c'},
  isTree =True, isRooted = True,
  isRegular = True
)

# 3-coloring on a rooted trees (degree not known i.e. not just binary)
# 12, 13, 23, 21, 31, 32 in automata-theoretic formalism
# cycle path classifier
cyclePathTreeProblem = GenericProblem(
  {'A a a a a', 'B b b b b', 'C c c c c'},
  {'A b', 'A c', 'B c', 'B a', 'C a', 'C b'} ,
  isTree =True, isRooted = True,
  isRegular = False
)

# -dir -n "{00, 1M}" -e "{01, 10, 11, MM}"
# --start-constr "{ 1 }" --end-constr "{ 0 }"
# cycle path classifier
cyclePathProblem = GenericProblem(
  {'A A', 'B M'},
  {'A B', 'B A', 'B B', 'M M'},
  leafConstraints = {'A'}, leafAllowAll = False, # leaf constraint = end-constr
  rootConstraints = {'B'}, rootAllowAll = False, # root constraint = start-constr
  isCycle = False, isPath = True, isDirected = True,
  isTree = False,
)

# -undir -n "{ 11, 22, 33 }" -e "{ 12, 21, 13, 31, 23, 32 }"
# cycle path classifier
cyclePathProblem = GenericProblem(
  {'A A', 'B B', 'C C'},
  {'A B', 'B A', 'A C', 'C A', 'B C', 'C B'},
  isCycle = True, isPath = False, isDirected = False,
  isTree = False
)


