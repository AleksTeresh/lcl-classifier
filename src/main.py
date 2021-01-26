import sys, getopt
from problem import GenericProblem, TlpProblem, BinaryRootedTreeProblem
from parser import parseConfigs
from cp_binding import classify as cpClassify
from rt_binding import classify as rtClassify

REtorProblem1 = GenericProblem(
  activeConstraints = ['M U U U', 'P P P P'],
  passiveConstraints = ['M UP UP UP', 'U U U U']
)

REtorProblem2 = GenericProblem(
  activeConstraints = ['M(W->B) S(W->B)(B->W)MP (W->B)(B->W) (W->B)(B->W)SUS'],
  passiveConstraints = ['(B->W) (W->B)(B->W) (W->B)(B->W)']
)
 
# AB CC BC
# AAA AAB AAC BCC ACC
# output: log* n
tlpProblem = GenericProblem(
  ['A B', 'C C', 'B C'],
  ['A A A', 'A A B', 'A A C', 'B C C', 'A C C']
)

# AA CC BC
# AAA AAB AAC BCC ACC
# output: O(1)
tlpProblem = GenericProblem(
  ['A A', 'C C', 'B C'],
  ['A A A', 'A A B', 'A A C', 'B C C', 'A C C']
)

# "111",
# "121",
# "131"
# "132"
# decider, tree-classification
binaryRootedTreeProblem = GenericProblem(
  ['a a a', 'b a a', 'c a a', 'c a b'],
  ['a a', 'b b', 'c c'],
  isTree = True, isRooted = True,
  isRegular = True
)

rtClassify(binaryRootedTreeProblem)

# "121",
# "132",
# "213"
# decider, tree-classification
binaryRootedTreeProblem = GenericProblem(
  ['b a a', 'c a b', 'a b c'],
  ['a a', 'b b', 'c c'],
  isTree = True, isRooted = True,
  isRegular = True
)

rtClassify(binaryRootedTreeProblem)

# "121",
# "131"
# "132"
# decider, tree-classification
binaryRootedTreeProblem = GenericProblem(
  ['b a a', 'c a a', 'c a b'],
  ['a a', 'b b', 'c c'],
  isTree = True, isRooted = True,
  isRegular = True
)

rtClassify(binaryRootedTreeProblem)

# 3-coloring on a rooted trees (degree not known i.e. not just binary)
# 12, 13, 23, 21, 31, 32 in automata-theoretic formalism
# cycle path classifier
cyclePathTreeProblem = GenericProblem(
  ['a a a a a', 'b b b b b', 'c c c c c'],
  ['a b', 'a c', 'b c', 'b a', 'c a', 'c b'] ,
  isTree =True, isRooted = True,
  isRegular = False
)

cpClassify(cyclePathTreeProblem)

# -undir -n "{00, 1M}" -e "{01, 10, 11, MM}"
# --start-constr "{ 1 }" --end-constr "{ 0 }"
# cycle path classifier
cyclePathProblem1 = GenericProblem(
  ['A A', 'B M'], # node constraints
  ['A B', 'B A', 'B B', 'M M'], # edge constraints
  leafConstraints = ['B'], leafAllowAll = False, # leaf constraint = end-constr
  rootConstraints = ['B'], rootAllowAll = False, # root constraint = start-constr
  isCycle = False, isPath = True, isDirected = False,
  isTree = False,
)

try:
  cpClassify(cyclePathProblem1)
except:
  pass

# -dir -n "{00, 1M}" -e "{01, 10, 11, MM}"
# --start-constr "{ 1 }" --end-constr "{ 0 }"
# cycle path classifier
cyclePathProblem2 = GenericProblem(
  ['A A', 'B M'], # node constraints
  ['A B', 'B A', 'B B', 'M M'], # edge constraints
  leafConstraints = ['B'], leafAllowAll = False, # leaf constraint = end-constr
  rootConstraints = ['B'], rootAllowAll = False, # root constraint = start-constr
  isCycle = False, isPath = True, isDirected = True,
  isTree = False,
)

cpClassify(cyclePathProblem2)

# -undir -n "{ 11, 22, 33 }" -e "{ 12, 21, 13, 31, 23, 32 }"
# cycle path classifier
cyclePathProblem = GenericProblem(
  ['A A', 'B B', 'C C'],
  ['A B', 'B A', 'A C', 'C A', 'B C', 'C B'],
  isCycle = True, isPath = False, isDirected = False,
  isTree = False
)

cpClassify(cyclePathProblem)
