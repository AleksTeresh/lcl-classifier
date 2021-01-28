import sys, getopt
from problem import GenericProblem, TlpProblem, BinaryRootedTreeProblem
from parser import parseConfigs
from classifier import classify

REtorProblem1 = GenericProblem(
  activeConstraints = ['M U U U', 'P P P P'],
  passiveConstraints = ['M UP UP UP', 'U U U U']
)

REtorProblem2 = GenericProblem(
  activeConstraints = ['M(W->B) S(W->B)(B->W)MP (W->B)(B->W) (W->B)(B->W)SUS'],
  passiveConstraints = ['(B->W) (W->B)(B->W) (W->B)(B->W)']
)

# const, 1 round solvable
REtorProblem3 = GenericProblem(
  ['M U U U', 'PM PM PM PM'],
  ['M UP UP UP', 'U U U U']
)
 
# AB, CC
# BBC, AAA, BBB, AAC, BCC
# output: log* n
tlpProblem1 = GenericProblem(
  ['A B', 'C C'],
  ['B B C', 'A A A', 'B B B', 'A A C', 'B C C']
)

# AA CC BC
# AAA AAB AAC BCC ACC
# output: O(1) 0
tlpProblem2 = GenericProblem(
  ['A A', 'C C', 'B C'],
  ['A A A', 'A A B', 'A A C', 'B C C', 'A C C']
)

# AC AB CC BC
# BB AC AB BC
# output: O(1) 1
tlpProblem3 = GenericProblem(
  ['A C', 'A B', 'C C', 'B C'],
  ['B B', 'A C', 'A B', 'B C']
)



# "111",
# "121",
# "131"
# "132"
# decider, tree-classification
# output: O(1)
binaryRootedTreeProblem1 = GenericProblem(
  ['a a a', 'b a a', 'c a a', 'c a b'],
  ['a a', 'b b', 'c c'],
  isTree = True, isRooted = True,
  isRegular = True
)



# "121",
# "132",
# "213"
# decider, tree-classification
# output: O(log n)
binaryRootedTreeProblem2 = GenericProblem(
  ['b a a', 'c a b', 'a b c'],
  ['a a', 'b b', 'c c'],
  isTree = True, isRooted = True,
  isRegular = True
)



# "121",
# "131"
# "132"
# decider, tree-classification
# output: unsolvable
binaryRootedTreeProblem3 = GenericProblem(
  ['b a a', 'c a a', 'c a b'],
  ['a a', 'b b', 'c c'],
  isTree = True, isRooted = True,
  isRegular = True
)



# 3-coloring on a rooted trees (degree not known i.e. not just binary)
# 12, 13, 23, 21, 31, 32 in automata-theoretic formalism
# cycle path classifier
cyclePathTreeProblem = GenericProblem(
  ['a a a a a', 'b b b b b', 'c c c c c'],
  ['a b', 'a c', 'b c', 'b a', 'c a', 'c b'] ,
  isTree =True, isRooted = True,
  isRegular = False
)



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



# -undir -n "{ 11, 22, 33 }" -e "{ 12, 21, 13, 31, 23, 32 }"
# cycle path classifier
cyclePathProblem = GenericProblem(
  ['A A', 'B B', 'C C'],
  ['A B', 'B A', 'A C', 'C A', 'B C', 'C B'],
  isCycle = True, isPath = False, isDirected = False,
  isTree = False
)


print(classify(tlpProblem1))
print(classify(tlpProblem2))
print(classify(tlpProblem3))
print(classify(binaryRootedTreeProblem1))
print(classify(binaryRootedTreeProblem2))
print(classify(binaryRootedTreeProblem3))
print(classify(cyclePathTreeProblem))
print(classify(cyclePathProblem1))
print(classify(cyclePathProblem2))
print(classify(cyclePathProblem))
