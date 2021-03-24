import unittest
import pickle
from .problem import GenericProblem, ProblemFlags, ProblemProps
from .generator import generate

class TestGenerator(unittest.TestCase):
    def __checkEquality(self, results, saved):
        self.assertEqual(len(results), len(saved))
        for r, s in zip(results, saved):
            self.assertEqual(r.activeConstraints, s.activeConstraints)
            self.assertEqual(r.passiveConstraints, s.passiveConstraints)
            self.assertEqual(r.leafConstraints, s.leafConstraints)
            self.assertEqual(r.rootConstraints, s.rootConstraints)
            self.assertEqual(r.leafAllowAll, s.leafAllowAll)
            self.assertEqual(r.rootAllowAll, s.rootAllowAll)
            self.assertEqual(r.flags.isTree, s.flags.isTree)
            self.assertEqual(r.flags.isCycle, s.flags.isCycle)
            self.assertEqual(r.flags.isPath, s.flags.isPath)
            self.assertEqual(r.flags.isDirectedOrRooted, s.flags.isDirectedOrRooted)
            self.assertEqual(r.flags.isRegular, s.flags.isRegular)

    def testGenerate1(self):
        activeDegree = 3
        passiveDegree = 2
        labelCount = 2
        activesAllSame = False
        passivesAllSame = True
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

        with open("test_data/problems1.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__checkEquality(ps, saved)

    def testGenerate2(self):
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

        with open("test_data/problems2.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__checkEquality(ps, saved)

    def testGenerate3(self):
        activeDegree = 2
        passiveDegree = 2
        labelCount = 2
        activesAllSame = False
        passivesAllSame = False
        flags = ProblemFlags(
            isTree=False,
            isCycle=False,
            isPath=True,
            isDirectedOrRooted=False,
        )

        ps = generate(
            activeDegree,
            passiveDegree,
            labelCount,
            activesAllSame,
            passivesAllSame,
            flags,
        )

        with open("test_data/problems3.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__checkEquality(ps, saved)

    def testGenerate4(self):
        activeDegree = 2
        passiveDegree = 2
        labelCount = 2
        activesAllSame = False
        passivesAllSame = False
        flags = ProblemFlags(
            isTree=False,
            isCycle=False,
            isPath=True,
            isDirectedOrRooted=True,
        )

        ps = generate(
            activeDegree,
            passiveDegree,
            labelCount,
            activesAllSame,
            passivesAllSame,
            flags,
        )

        with open("test_data/problems4.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__checkEquality(ps, saved)

