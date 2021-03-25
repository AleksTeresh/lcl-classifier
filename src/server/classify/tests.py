import unittest
import pickle
from .batch_classify import batchClassify
from .classifier import classify
from complexity import *
from problem import GenericProblem, ProblemFlags, ProblemProps
from problem import generate

class TestBatchClassifier(unittest.TestCase):
    def __checkEquality(self, results, saved):
        self.assertEqual(len(results), len(saved))
        for r, s in zip(results, saved):
            self.assertEqual(r.randLowerBound, s.randLowerBound)
            self.assertEqual(r.randUpperBound, s.randUpperBound)
            self.assertEqual(r.detLowerBound, s.detLowerBound)
            self.assertEqual(r.detUpperBound, s.detUpperBound)

    def testClassifier1(self):
        activeDegree = 2
        passiveDegree = 2
        labelCount = 2
        activesAllSame = False
        passivesAllSame = False
        flags = ProblemFlags(
            isTree=False, isCycle=False, isPath=True, isDirectedOrRooted=False
        )
        ps = generate(
            activeDegree,
            passiveDegree,
            labelCount,
            activesAllSame,
            passivesAllSame,
            flags,
        )
        results = batchClassify(ps)
        with open("test_data/classifications1.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__checkEquality(results, saved)

    def testClassifier2(self):
        activeDegree = 2
        passiveDegree = 2
        labelCount = 2
        activesAllSame = False
        passivesAllSame = False
        flags = ProblemFlags(
            isTree=False, isCycle=False, isPath=True, isDirectedOrRooted=True
        )
        ps = generate(
            activeDegree,
            passiveDegree,
            labelCount,
            activesAllSame,
            passivesAllSame,
            flags,
        )
        results = batchClassify(ps)
        with open("test_data/classifications2.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__checkEquality(results, saved)

    def testClassifier3(self):
        activeDegree = 2
        passiveDegree = 2
        labelCount = 3
        activesAllSame = False
        passivesAllSame = False
        flags = ProblemFlags(
            isTree=False, isCycle=False, isPath=True, isDirectedOrRooted=False
        )
        ps = generate(
            activeDegree,
            passiveDegree,
            labelCount,
            activesAllSame,
            passivesAllSame,
            flags,
        )
        results = batchClassify(ps)
        with open("test_data/classifications3.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__checkEquality(results, saved)

    def testClassifier4(self):
        activeDegree = 3
        passiveDegree = 2
        labelCount = 2
        activesAllSame = False
        passivesAllSame = False
        flags = ProblemFlags(
            isTree=True, isCycle=False, isPath=False, isDirectedOrRooted=False
        )
        ps = generate(
            activeDegree,
            passiveDegree,
            labelCount,
            activesAllSame,
            passivesAllSame,
            flags,
        )
        results = batchClassify(ps)
        with open("test_data/classifications4.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__checkEquality(results, saved)

    def testClassifier5(self):
        activeDegree = 3
        passiveDegree = 2
        labelCount = 2
        activesAllSame = False
        passivesAllSame = False
        flags = ProblemFlags(
            isTree=True, isCycle=False, isPath=False, isDirectedOrRooted=True
        )
        ps = generate(
            activeDegree,
            passiveDegree,
            labelCount,
            activesAllSame,
            passivesAllSame,
            flags,
        )
        results = batchClassify(ps)
        with open("test_data/classifications5.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__checkEquality(results, saved)

class TestClassifier(unittest.TestCase):
    def testRe1(self):
        REtorProblem1 = GenericProblem(
            activeConstraints=["M U U U", "P P P P"],
            passiveConstraints=["M UP UP UP", "U U U U"],
        )
        res = classify(REtorProblem1)
        self.assertEqual(res.detLowerBound, CONST)
        self.assertEqual(res.detUpperBound, UNSOLVABLE)
        self.assertEqual(res.randUpperBound, UNSOLVABLE)
        self.assertEqual(res.randLowerBound, CONST)

    def testRe2(self):
        REtorProblem2 = GenericProblem(
            activeConstraints=["A AB AB AB"], passiveConstraints=["B AB AB"]
        )
        res = classify(REtorProblem2)
        self.assertEqual(res.detLowerBound, LOG)
        self.assertEqual(res.detUpperBound, UNSOLVABLE)
        self.assertEqual(res.randUpperBound, UNSOLVABLE)
        self.assertEqual(res.randLowerBound, LOGLOG)

    def testRe3(self):
        # const, 1 round solvable
        REtorProblem3 = GenericProblem(
            ["M U U U", "PM PM PM PM"], ["M UP UP UP", "U U U U"]
        )
        res = classify(REtorProblem3)
        self.assertEqual(res.detLowerBound, CONST)
        self.assertEqual(res.detUpperBound, CONST)
        self.assertEqual(res.randUpperBound, CONST)
        self.assertEqual(res.randLowerBound, CONST)

    def testTlp1(self):
        # AB, CC
        # BBC, AAA, BBB, AAC, BCC
        # output: log* n
        tlpProblem1 = GenericProblem(
            ["A B", "C C"], ["B B C", "A A A", "B B B", "A A C", "B C C"]
        )
        res = classify(tlpProblem1)
        self.assertEqual(res.detLowerBound, ITERATED_LOG)
        self.assertEqual(res.detUpperBound, ITERATED_LOG)
        self.assertEqual(res.randUpperBound, ITERATED_LOG)
        self.assertEqual(res.randLowerBound, ITERATED_LOG)

    def testTlp2(self):
        # AA CC BC
        # AAA AAB AAC BCC ACC
        # output: O(1) 0
        tlpProblem2 = GenericProblem(
            ["A A", "C C", "B C"], ["A A A", "A A B", "A A C", "B C C", "A C C"]
        )
        res = classify(tlpProblem2)
        self.assertEqual(res.detLowerBound, CONST)
        self.assertEqual(res.detUpperBound, CONST)
        self.assertEqual(res.randUpperBound, CONST)
        self.assertEqual(res.randLowerBound, CONST)

    def testTlp3(self):
        # AC AB CC BC
        # BB AC AB BC
        # output: O(1) 1
        tlpProblem3 = GenericProblem(
            ["A C", "A B", "C C", "B C"], ["B B", "A C", "A B", "B C"]
        )
        res = classify(tlpProblem3)
        self.assertEqual(res.detLowerBound, CONST)
        self.assertEqual(res.detUpperBound, CONST)
        self.assertEqual(res.randUpperBound, CONST)
        self.assertEqual(res.randLowerBound, CONST)

    def testTlp4(self):
        # AB, CC
        # BBC, AAA, BBB, AAC, BCC
        # output: log* n
        tlpProblem1 = GenericProblem(
            ["1 2", "3 3"], ["2 2 3", "1 1 1", "2 2 2", "1 1 3", "2 3 3"]
        )
        res = classify(tlpProblem1)
        self.assertEqual(res.detLowerBound, ITERATED_LOG)
        self.assertEqual(res.detUpperBound, ITERATED_LOG)
        self.assertEqual(res.randUpperBound, ITERATED_LOG)
        self.assertEqual(res.randLowerBound, ITERATED_LOG)

    def testBrt0(self):
        binaryRootedTreeProblem0 = GenericProblem(
            ["a : a a"], ["a : a"], flags=ProblemFlags(isTree=True)
        )
        res = classify(binaryRootedTreeProblem0)
        self.assertEqual(res.detLowerBound, CONST)
        self.assertEqual(res.detUpperBound, CONST)
        self.assertEqual(res.randUpperBound, CONST)
        self.assertEqual(res.randLowerBound, CONST)

    def testBrt1(self):
        # "111",
        # "121",
        # "131"
        # "132"
        # decider, tree-classification
        # output: O(1)
        binaryRootedTreeProblem1 = GenericProblem(
            ["a : a a", "b : a a", "c : a a", "c : a b"],
            ["a : a", "b : b", "c : c"],
            flags=ProblemFlags(isTree=True),
        )
        res = classify(binaryRootedTreeProblem1)
        self.assertEqual(res.detLowerBound, CONST)
        self.assertEqual(res.detUpperBound, CONST)
        self.assertEqual(res.randUpperBound, CONST)
        self.assertEqual(res.randLowerBound, CONST)

    def testBrt2(self):
        # "121",
        # "132",
        # "213"
        # decider, tree-classification
        # output: O(log n)
        binaryRootedTreeProblem2 = GenericProblem(
            ["b : a a", "c : a b", "a : b c"],
            ["a : a", "b : b", "c : c"],
            flags=ProblemFlags(isTree=True),
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
            ["b : a a", "c : a a", "c : a b"],
            ["a : a", "b : b", "c : c"],
            flags=ProblemFlags(isTree=True),
        )
        res = classify(binaryRootedTreeProblem3)
        self.assertEqual(res.detLowerBound, UNSOLVABLE)
        self.assertEqual(res.detUpperBound, UNSOLVABLE)
        self.assertEqual(res.randUpperBound, UNSOLVABLE)
        self.assertEqual(res.randLowerBound, UNSOLVABLE)

    def testCyclePath1(self):
        # 3-coloring on a rooted trees (degree not known i.e. not just binary)
        # 12, 13, 23, 21, 31, 32 in automata-theoretic formalism
        # cycle path classifier
        cyclePathTreeProblem1 = GenericProblem(
            ["a : a a a a", "b : b b b b", "c : c c c c"],
            ["a : b", "a : c", "b : c", "b : a", "c : a", "c : b"],
            flags=ProblemFlags(
                isTree=True,
            ),
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
            ["A A", "B M"],  # node constraints
            ["A B", "B A", "B B", "M M"],  # edge constraints
            leafConstraints=["B"],
            leafAllowAll=False,  # leaf constraint = end-constr
            rootConstraints=["B"],
            rootAllowAll=False,  # root constraint = start-constr
            flags=ProblemFlags(
                isCycle=False,
                isPath=True,
                isTree=False,
            ),
        )
        res = classify(cyclePathProblem2)
        self.assertEqual(res.detLowerBound, ITERATED_LOG)
        self.assertEqual(res.detUpperBound, ITERATED_LOG)
        self.assertEqual(res.randUpperBound, ITERATED_LOG)
        self.assertEqual(res.randLowerBound, ITERATED_LOG)

    def testCyclePath3(self):
        # -dir -n "{00, 1M}" -e "{01, 10, 11, MM}"
        # --start-constr "{ 1 }" --end-constr "{ 0 }"
        # cycle path classifier
        cyclePathProblem3 = GenericProblem(
            ["A : A", "B : M"],  # node constraints
            ["A : B", "B : A", "B : B", "M : M"],  # edge constraints
            leafConstraints=["B"],
            leafAllowAll=False,  # leaf constraint = end-constr
            rootConstraints=["B"],
            rootAllowAll=False,  # root constraint = start-constr
            flags=ProblemFlags(
                isCycle=False,
                isPath=True,
                isTree=False,
            ),
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
            ["A A", "B B", "C C"],
            ["A B", "B A", "A C", "C A", "B C", "C B"],
            flags=ProblemFlags(isCycle=True, isPath=False, isTree=False),
        )
        res = classify(cyclePathProblem4)
        self.assertEqual(res.detLowerBound, ITERATED_LOG)
        self.assertEqual(res.detUpperBound, ITERATED_LOG)
        self.assertEqual(res.randUpperBound, ITERATED_LOG)
        self.assertEqual(res.randLowerBound, ITERATED_LOG)
