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
 
