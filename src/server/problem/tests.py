import sys
from typing import List
import unittest
import pickle
from .problem import ProblemFlags, GenericProblem
from .generator import generate

OVERWRITE = False


def saveToFile(filePath: str, problems: List[GenericProblem]) -> None:
    with open(filePath, "wb") as handle:
        pickle.dump(problems, handle)


def loadFromFile(filePath: str) -> List[GenericProblem]:
    with open(filePath, "rb") as handle:
        r = pickle.load(handle)
        return r


class TestGenerator(unittest.TestCase):
    def __check_equality(self, results, saved):
        self.assertEqual(len(results), len(saved))
        for r, s in zip(sorted(results), sorted(saved)):
            self.assertEqual(r.active_constraints, s.active_constraints)
            self.assertEqual(r.passive_constraints, s.passive_constraints)
            self.assertEqual(r.leaf_constraints, s.leaf_constraints)
            self.assertEqual(r.root_constraints, s.root_constraints)
            self.assertEqual(r.leaf_allow_all, s.leaf_allow_all)
            self.assertEqual(r.root_allow_all, s.root_allow_all)
            self.assertEqual(r.flags.is_tree, s.flags.is_tree)
            self.assertEqual(r.flags.is_cycle, s.flags.is_cycle)
            self.assertEqual(r.flags.is_path, s.flags.is_path)
            self.assertEqual(
                r.flags.is_directed_or_rooted, s.flags.is_directed_or_rooted
            )
            self.assertEqual(r.flags.is_regular, s.flags.is_regular)

    def __runTest(self, filePath: str, ps: List[GenericProblem]) -> None:
        overwrite = OVERWRITE
        if overwrite:
            saveToFile(filePath, ps)
        else:
            saved = loadFromFile(filePath)
            self.__check_equality(ps, saved)

    def test_generate1(self):
        active_degree = 3
        passive_degree = 2
        label_count = 2
        actives_all_same = False
        passives_all_same = True
        flags = ProblemFlags(
            is_tree=True, is_cycle=False, is_path=False, is_directed_or_rooted=True
        )

        ps = generate(
            active_degree,
            passive_degree,
            label_count,
            actives_all_same,
            passives_all_same,
            flags,
        )
        self.__runTest("test_data/problems1.pickle", ps)

    def test_generate2(self):
        active_degree = 3
        passive_degree = 2
        label_count = 2
        actives_all_same = False
        passives_all_same = False
        flags = ProblemFlags(
            is_tree=True, is_cycle=False, is_path=False, is_directed_or_rooted=False
        )

        ps = generate(
            active_degree,
            passive_degree,
            label_count,
            actives_all_same,
            passives_all_same,
            flags,
        )
        self.__runTest("test_data/problems2.pickle", ps)

    def test_generate3(self):
        active_degree = 2
        passive_degree = 2
        label_count = 2
        actives_all_same = False
        passives_all_same = False
        flags = ProblemFlags(
            is_tree=False,
            is_cycle=False,
            is_path=True,
            is_directed_or_rooted=False,
        )

        ps = generate(
            active_degree,
            passive_degree,
            label_count,
            actives_all_same,
            passives_all_same,
            flags,
        )
        self.__runTest("test_data/problems3.pickle", ps)

    def test_generate4(self):
        active_degree = 2
        passive_degree = 2
        label_count = 2
        actives_all_same = False
        passives_all_same = False
        flags = ProblemFlags(
            is_tree=False,
            is_cycle=False,
            is_path=True,
            is_directed_or_rooted=True,
        )

        ps = generate(
            active_degree,
            passive_degree,
            label_count,
            actives_all_same,
            passives_all_same,
            flags,
        )
        self.__runTest("test_data/problems4.pickle", ps)
