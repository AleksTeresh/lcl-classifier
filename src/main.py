import sys, getopt
from .problem import GenericProblem, TlpProblem, BinaryRootedTreeProblem
from cyclepath_classifier import classify, Problem as CyclePathProblem

REtorProblem = GenericProblem(
  {'M U U U', 'P P P P'}, False,
  {'M UP UP UP', 'U U U U'}, False,
  {}, True,
  {}, True,
  False, False, False,
  True, False,
  True,
  True
)
 
# AB CC BC
# AAA AAB AAC BCC ACC
tlpProblem = GenericProblem(
  {'A B', 'C C', 'B C'}, False,
  {'A A A', 'A A B', 'A A C', 'B C C', 'A C C'}, False,
  {}, True,
  {}, True,
  False, False, False,
  True, False,
  True,
  True
)

# "111",
# "121",
# "131"
# "132"
# decider, tree-classification
binaryRootedTreeProblem = GenericProblem(
  {'A a a', 'B a a', 'C a a', 'C a b'}, False,
  {'A a', 'B b', 'C c'}, False,
  {}, True,
  {}, True,
  False, False, False,
  True, True,
  True,
  True
)


# 3-coloring on a rooted trees (degree not known i.e. not just binary)
# 12, 13, 23, 21, 31, 32 in automata-theoretic formalism
# cycle path classifier
cyclePathTreeProblem = GenericProblem(
  {'A a a a a', 'B b b b b', 'C c c c c'}, False,
  {'A b', 'A c', 'B c', 'B a', 'C a', 'C b'} , False,
  {}, True,
  {}, True,
  False, False, False,
  True, True,
  True,
  True
)

# -dir -n "{00, 1M}" -e "{01, 10, 11, MM}"
# --start-constr "{ 1 }" --end-constr "{ 0 }"
# cycle path classifier
cyclePathProblem = GenericProblem(
  {'A A', 'B M'}, False,
  {'A B', 'B A', 'B B', 'M M'} , False,
  {'A'}, False, # leaf constraint = end-constr
  {'B'}, False, # root constraint = start-constr
  False, True, True,
  False, False,
  False,
  True
)

# -undir -n "{ 11, 22, 33 }" -e "{ 12, 21, 13, 31, 23, 32 }"
# cycle path classifier
cyclePathProblem = GenericProblem(
  {'A A', 'B B', 'C C'}, False,
  {'A B', 'B A', 'A C', 'C A', 'B C', 'C B'} , False,
  {}, True, # leaf constraint = end-constr
  {}, True, # root constraint = start-constr
  True, False, False,
  False, False,
  False,
  True
)


mmProblem = GenericProblem()

misProblem = GenericProblem()

vertexColoring = GenericProblem()

edgeColoring = GenericProblem()
