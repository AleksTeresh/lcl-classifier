import unittest
import pickle
from .problem import GenericProblem, ProblemFlags, ProblemProps
from .generator import generate


class TestGenerator(unittest.TestCase):
    def __check_equality(self, results, saved):
        self.assertEqual(len(results), len(saved))
        for r, s in zip(results, saved):
            self.assertEqual(r.active_constraints, s.activeConstraints)
            self.assertEqual(r.passive_constraints, s.passiveConstraints)
            self.assertEqual(r.leaf_constraints, s.leafConstraints)
            self.assertEqual(r.root_constraints, s.rootConstraints)
            self.assertEqual(r.leaf_allow_all, s.leafAllowAll)
            self.assertEqual(r.root_allow_all, s.rootAllowAll)
            self.assertEqual(r.flags.is_tree, s.flags.isTree)
            self.assertEqual(r.flags.is_cycle, s.flags.isCycle)
            self.assertEqual(r.flags.is_path, s.flags.isPath)
            self.assertEqual(r.flags.is_directed_or_rooted, s.flags.isDirectedOrRooted)
            self.assertEqual(r.flags.is_regular, s.flags.isRegular)

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

        with open("test_data/problems1.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__check_equality(ps, saved)

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

        with open("test_data/problems2.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__check_equality(ps, saved)

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

        with open("test_data/problems3.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__check_equality(ps, saved)

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

        with open("test_data/problems4.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__check_equality(ps, saved)
