import unittest
from problem import GenericProblem, TlpProblem, BinaryRootedTreeProblem
from parser import parseConfigs
from classifier import classify
from complexity import *

class TestClassifier(unittest.TestCase):
  def testTlp1(self):
    # AB, CC
    # BBC, AAA, BBB, AAC, BCC
    # output: log* n
    tlpProblem1 = GenericProblem(
      ['A B', 'C C'],
      ['B B C', 'A A A', 'B B B', 'A A C', 'B C C']
    )
    res = classify(tlpProblem1)
    self.assertEqual(res.detLowerBound, ITERATED_LOG)
    self.assertEqual(res.detUpperBound, ITERATED_LOG)
    self.assertEqual(res.randUpperBound, ITERATED_LOG)
    self.assertEqual(res.randLowerBound, UNKNOWN)

  def testTlp2(self):
    # AA CC BC
    # AAA AAB AAC BCC ACC
    # output: O(1) 0
    tlpProblem2 = GenericProblem(
      ['A A', 'C C', 'B C'],
      ['A A A', 'A A B', 'A A C', 'B C C', 'A C C']
    )
    res = classify(tlpProblem2)
    self.assertEqual(res.detLowerBound, CONST)
    self.assertEqual(res.detUpperBound, CONST)
    self.assertEqual(res.randUpperBound, CONST)
    self.assertEqual(res.randLowerBound, UNKNOWN) #TODO: change to const

  def testTlp3(self):
    # AC AB CC BC
    # BB AC AB BC
    # output: O(1) 1
    tlpProblem3 = GenericProblem(
      ['A C', 'A B', 'C C', 'B C'],
      ['B B', 'A C', 'A B', 'B C']
    )
    res = classify(tlpProblem3)
    self.assertEqual(res.detLowerBound, CONST)
    self.assertEqual(res.detUpperBound, CONST)
    self.assertEqual(res.randUpperBound, CONST)
    self.assertEqual(res.randLowerBound, UNKNOWN) #TODO: change to const

  def testBrt1(self):
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
    res = classify(binaryRootedTreeProblem1)
    self.assertEqual(res.detLowerBound, CONST)
    self.assertEqual(res.detUpperBound, ITERATED_LOG) #TODO: change to const
    self.assertEqual(res.randUpperBound, CONST)
    self.assertEqual(res.randLowerBound, CONST)

  def testBrt2(self):
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
    res = classify(binaryRootedTreeProblem2)
    self.assertEqual(res.detLowerBound, LOG)
    self.assertEqual(res.detUpperBound, LOG)
    self.assertEqual(res.randUpperBound, LOG)
    self.assertEqual(res.randLowerBound, LOG)

  def testBrt3(self):
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
    res = classify(binaryRootedTreeProblem3)
    self.assertEqual(res.detLowerBound, UNSOLVABLE)
    self.assertEqual(res.detUpperBound, UNKNOWN) #TODO: change to UNSOLVABLE
    self.assertEqual(res.randUpperBound, UNSOLVABLE)
    self.assertEqual(res.randLowerBound, UNSOLVABLE)

  def testCyclePath1(self):
    # 3-coloring on a rooted trees (degree not known i.e. not just binary)
    # 12, 13, 23, 21, 31, 32 in automata-theoretic formalism
    # cycle path classifier
    cyclePathTreeProblem1 = GenericProblem(
      ['a a a a a', 'b b b b b', 'c c c c c'],
      ['a b', 'a c', 'b c', 'b a', 'c a', 'c b'] ,
      isTree =True, isRooted = True,
      isRegular = False
    )
    res = classify(cyclePathTreeProblem1)
    self.assertEqual(res.detLowerBound, ITERATED_LOG)
    self.assertEqual(res.detUpperBound, ITERATED_LOG)
    self.assertEqual(res.randUpperBound, ITERATED_LOG)
    self.assertEqual(res.randLowerBound, ITERATED_LOG)

  def testCyclePath2(self):
    # -undir -n "{00, 1M}" -e "{01, 10, 11, MM}"
    # --start-constr "{ 1 }" --end-constr "{ 0 }"
    # cycle path classifier
    cyclePathProblem2 = GenericProblem(
      ['A A', 'B M'], # node constraints
      ['A B', 'B A', 'B B', 'M M'], # edge constraints
      leafConstraints = ['B'], leafAllowAll = False, # leaf constraint = end-constr
      rootConstraints = ['B'], rootAllowAll = False, # root constraint = start-constr
      isCycle = False, isPath = True, isDirected = False,
      isTree = False,
    )
    res = classify(cyclePathProblem2)
    self.assertEqual(res.detLowerBound, CONST)
    self.assertEqual(res.detUpperBound, UNKNOWN)
    self.assertEqual(res.randUpperBound, UNKNOWN)
    self.assertEqual(res.randLowerBound, CONST)

  def testCyclePath3(self):
    # -dir -n "{00, 1M}" -e "{01, 10, 11, MM}"
    # --start-constr "{ 1 }" --end-constr "{ 0 }"
    # cycle path classifier
    cyclePathProblem3 = GenericProblem(
      ['A A', 'B M'], # node constraints
      ['A B', 'B A', 'B B', 'M M'], # edge constraints
      leafConstraints = ['B'], leafAllowAll = False, # leaf constraint = end-constr
      rootConstraints = ['B'], rootAllowAll = False, # root constraint = start-constr
      isCycle = False, isPath = True, isDirected = True,
      isTree = False,
    )
    res = classify(cyclePathProblem3)
    self.assertEqual(res.detLowerBound, CONST)
    self.assertEqual(res.detUpperBound, CONST)
    self.assertEqual(res.randUpperBound, CONST)
    self.assertEqual(res.randLowerBound, CONST)

  def testCyclePath4(self):
    # -undir -n "{ 11, 22, 33 }" -e "{ 12, 21, 13, 31, 23, 32 }"
    # cycle path classifier
    cyclePathProblem4 = GenericProblem(
      ['A A', 'B B', 'C C'],
      ['A B', 'B A', 'A C', 'C A', 'B C', 'C B'],
      isCycle = True, isPath = False, isDirected = False,
      isTree = False
    )
    res = classify(cyclePathProblem4)
    self.assertEqual(res.detLowerBound, ITERATED_LOG)
    self.assertEqual(res.detUpperBound, ITERATED_LOG)
    self.assertEqual(res.randUpperBound, ITERATED_LOG)
    self.assertEqual(res.randLowerBound, ITERATED_LOG)

unittest.main()