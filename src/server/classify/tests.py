import unittest
import pickle
from .batch_classify import batch_classify
from .classifier import classify
from complexity import CONST, ITERATED_LOG, LOG, UNSOLVABLE, LOGLOG
from problem import GenericProblem, ProblemFlags
from problem import generate


class TestBatchClassifier(unittest.TestCase):
    def __check_equality(self, results, saved):
        self.assertEqual(len(results), len(saved))
        for r, s in zip(results, saved):
            self.assertEqual(r.rand_lower_bound, s.randLowerBound)
            self.assertEqual(r.rand_upper_bound, s.randUpperBound)
            self.assertEqual(r.det_lower_bound, s.detLowerBound)
            self.assertEqual(r.det_upper_bound, s.detUpperBound)

    def test_classifier1(self):
        active_degree = 2
        passive_degree = 2
        label_count = 2
        actives_all_same = False
        passives_all_same = False
        flags = ProblemFlags(
            is_tree=False, is_cycle=False, is_path=True, is_directed_or_rooted=False
        )
        ps = generate(
            active_degree,
            passive_degree,
            label_count,
            actives_all_same,
            passives_all_same,
            flags,
        )
        results = batch_classify(ps)
        with open("test_data/classifications1.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__check_equality(results, saved)

    def test_classifier2(self):
        active_degree = 2
        passive_degree = 2
        label_count = 2
        actives_all_same = False
        passives_all_same = False
        flags = ProblemFlags(
            is_tree=False, is_cycle=False, is_path=True, is_directed_or_rooted=True
        )
        ps = generate(
            active_degree,
            passive_degree,
            label_count,
            actives_all_same,
            passives_all_same,
            flags,
        )
        results = batch_classify(ps)
        with open("test_data/classifications2.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__check_equality(results, saved)

    def test_classifier3(self):
        active_degree = 2
        passive_degree = 2
        label_count = 3
        actives_all_same = False
        passives_all_same = False
        flags = ProblemFlags(
            is_tree=False, is_cycle=False, is_path=True, is_directed_or_rooted=False
        )
        ps = generate(
            active_degree,
            passive_degree,
            label_count,
            actives_all_same,
            passives_all_same,
            flags,
        )
        results = batch_classify(ps)
        with open("test_data/classifications3.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__check_equality(results, saved)

    def test_classifier4(self):
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
        results = batch_classify(ps)
        with open("test_data/classifications4.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__check_equality(results, saved)

    def test_classifier5(self):
        active_degree = 3
        passive_degree = 2
        label_count = 2
        actives_all_same = False
        passives_all_same = False
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
        results = batch_classify(ps)
        with open("test_data/classifications5.pickle", "rb") as handle:
            saved = pickle.load(handle)
            self.__check_equality(results, saved)


class TestClassifier(unittest.TestCase):
    def test_re1(self):
        REtorProblem1 = GenericProblem(
            active_constraints=["M U U U", "P P P P"],
            passive_constraints=["M UP UP UP", "U U U U"],
        )
        res = classify(REtorProblem1)
        self.assertEqual(res.det_lower_bound, CONST)
        self.assertEqual(res.det_upper_bound, UNSOLVABLE)
        self.assertEqual(res.rand_upper_bound, UNSOLVABLE)
        self.assertEqual(res.rand_lower_bound, CONST)

    def test_re2(self):
        REtorProblem2 = GenericProblem(
            active_constraints=["A AB AB AB"], passive_constraints=["B AB AB"]
        )
        res = classify(REtorProblem2)
        self.assertEqual(res.det_lower_bound, LOG)
        self.assertEqual(res.det_upper_bound, UNSOLVABLE)
        self.assertEqual(res.rand_upper_bound, UNSOLVABLE)
        self.assertEqual(res.rand_lower_bound, LOGLOG)

    def test_re3(self):
        # const, 1 round solvable
        REtorProblem3 = GenericProblem(
            ["M U U U", "PM PM PM PM"], ["M UP UP UP", "U U U U"]
        )
        res = classify(REtorProblem3)
        self.assertEqual(res.det_lower_bound, CONST)
        self.assertEqual(res.det_upper_bound, CONST)
        self.assertEqual(res.rand_upper_bound, CONST)
        self.assertEqual(res.rand_lower_bound, CONST)

    def test_tlp1(self):
        # AB, CC
        # BBC, AAA, BBB, AAC, BCC
        # output: log* n
        tlp_problem1 = GenericProblem(
            ["A B", "C C"], ["B B C", "A A A", "B B B", "A A C", "B C C"]
        )
        res = classify(tlp_problem1)
        self.assertEqual(res.det_lower_bound, ITERATED_LOG)
        self.assertEqual(res.det_upper_bound, ITERATED_LOG)
        self.assertEqual(res.rand_upper_bound, ITERATED_LOG)
        self.assertEqual(res.rand_lower_bound, ITERATED_LOG)

    def test_tlp2(self):
        # AA CC BC
        # AAA AAB AAC BCC ACC
        # output: O(1) 0
        tlp_problem2 = GenericProblem(
            ["A A", "C C", "B C"], ["A A A", "A A B", "A A C", "B C C", "A C C"]
        )
        res = classify(tlp_problem2)
        self.assertEqual(res.det_lower_bound, CONST)
        self.assertEqual(res.det_upper_bound, CONST)
        self.assertEqual(res.rand_upper_bound, CONST)
        self.assertEqual(res.rand_lower_bound, CONST)

    def test_tlp3(self):
        # AC AB CC BC
        # BB AC AB BC
        # output: O(1) 1
        tlp_problem3 = GenericProblem(
            ["A C", "A B", "C C", "B C"], ["B B", "A C", "A B", "B C"]
        )
        res = classify(tlp_problem3)
        self.assertEqual(res.det_lower_bound, CONST)
        self.assertEqual(res.det_upper_bound, CONST)
        self.assertEqual(res.rand_upper_bound, CONST)
        self.assertEqual(res.rand_lower_bound, CONST)

    def test_tlp4(self):
        # AB, CC
        # BBC, AAA, BBB, AAC, BCC
        # output: log* n
        tlp_problem1 = GenericProblem(
            ["1 2", "3 3"], ["2 2 3", "1 1 1", "2 2 2", "1 1 3", "2 3 3"]
        )
        res = classify(tlp_problem1)
        self.assertEqual(res.det_lower_bound, ITERATED_LOG)
        self.assertEqual(res.det_upper_bound, ITERATED_LOG)
        self.assertEqual(res.rand_upper_bound, ITERATED_LOG)
        self.assertEqual(res.rand_lower_bound, ITERATED_LOG)

    def test_brt0(self):
        binary_rooted_tree_problem0 = GenericProblem(
            ["a : a a"], ["a : a"], flags=ProblemFlags(is_tree=True)
        )
        res = classify(binary_rooted_tree_problem0)
        self.assertEqual(res.det_lower_bound, CONST)
        self.assertEqual(res.det_upper_bound, CONST)
        self.assertEqual(res.rand_upper_bound, CONST)
        self.assertEqual(res.rand_lower_bound, CONST)

    def test_brt1(self):
        # "111",
        # "121",
        # "131"
        # "132"
        # decider, tree-classification
        # output: O(1)
        binary_rooted_tree_problem1 = GenericProblem(
            ["a : a a", "b : a a", "c : a a", "c : a b"],
            ["a : a", "b : b", "c : c"],
            flags=ProblemFlags(is_tree=True),
        )
        res = classify(binary_rooted_tree_problem1)
        self.assertEqual(res.det_lower_bound, CONST)
        self.assertEqual(res.det_upper_bound, CONST)
        self.assertEqual(res.rand_upper_bound, CONST)
        self.assertEqual(res.rand_lower_bound, CONST)

    def test_brt2(self):
        # "121",
        # "132",
        # "213"
        # decider, tree-classification
        # output: O(log n)
        binary_rooted_tree_problem2 = GenericProblem(
            ["b : a a", "c : a b", "a : b c"],
            ["a : a", "b : b", "c : c"],
            flags=ProblemFlags(is_tree=True),
        )
        res = classify(binary_rooted_tree_problem2)
        self.assertEqual(res.det_lower_bound, LOG)
        self.assertEqual(res.det_upper_bound, LOG)
        self.assertEqual(res.rand_upper_bound, LOG)
        self.assertEqual(res.rand_lower_bound, LOG)

    def test_brt3(self):
        # "121",
        # "131"
        # "132"
        # decider, tree-classification
        # output: unsolvable
        binary_rooted_tree_problem3 = GenericProblem(
            ["b : a a", "c : a a", "c : a b"],
            ["a : a", "b : b", "c : c"],
            flags=ProblemFlags(is_tree=True),
        )
        res = classify(binary_rooted_tree_problem3)
        self.assertEqual(res.det_lower_bound, UNSOLVABLE)
        self.assertEqual(res.det_upper_bound, UNSOLVABLE)
        self.assertEqual(res.rand_upper_bound, UNSOLVABLE)
        self.assertEqual(res.rand_lower_bound, UNSOLVABLE)

    def test_cycle_path1(self):
        # 3-coloring on a rooted trees (degree not known i.e. not just binary)
        # 12, 13, 23, 21, 31, 32 in automata-theoretic formalism
        # cycle path classifier
        cycle_path_tree_problem1 = GenericProblem(
            ["a : a a a a", "b : b b b b", "c : c c c c"],
            ["a : b", "a : c", "b : c", "b : a", "c : a", "c : b"],
            flags=ProblemFlags(
                is_tree=True,
            ),
        )
        res = classify(cycle_path_tree_problem1)
        self.assertEqual(res.det_lower_bound, ITERATED_LOG)
        self.assertEqual(res.det_upper_bound, ITERATED_LOG)
        self.assertEqual(res.rand_upper_bound, ITERATED_LOG)
        self.assertEqual(res.rand_lower_bound, ITERATED_LOG)

    def test_cycle_path2(self):
        # -undir -n "{00, 1M}" -e "{01, 10, 11, MM}"
        # --start-constr "{ 1 }" --end-constr "{ 0 }"
        # cycle path classifier
        cycle_path_problem2 = GenericProblem(
            ["A A", "B M"],  # node constraints
            ["A B", "B A", "B B", "M M"],  # edge constraints
            leaf_constraints=["B"],
            leaf_allow_all=False,  # leaf constraint = end-constr
            root_constraints=["B"],
            root_allow_all=False,  # root constraint = start-constr
            flags=ProblemFlags(
                is_cycle=False,
                is_path=True,
                is_tree=False,
            ),
        )
        res = classify(cycle_path_problem2)
        self.assertEqual(res.det_lower_bound, ITERATED_LOG)
        self.assertEqual(res.det_upper_bound, ITERATED_LOG)
        self.assertEqual(res.rand_upper_bound, ITERATED_LOG)
        self.assertEqual(res.rand_lower_bound, ITERATED_LOG)

    def test_cycle_path3(self):
        # -dir -n "{00, 1M}" -e "{01, 10, 11, MM}"
        # --start-constr "{ 1 }" --end-constr "{ 0 }"
        # cycle path classifier
        cycle_path_problem3 = GenericProblem(
            ["A : A", "B : M"],  # node constraints
            ["A : B", "B : A", "B : B", "M : M"],  # edge constraints
            leaf_constraints=["B"],
            leaf_allow_all=False,  # leaf constraint = end-constr
            root_constraints=["B"],
            root_allow_all=False,  # root constraint = start-constr
            flags=ProblemFlags(
                is_cycle=False,
                is_path=True,
                is_tree=False,
            ),
        )
        res = classify(cycle_path_problem3)
        self.assertEqual(res.det_lower_bound, CONST)
        self.assertEqual(res.det_upper_bound, CONST)
        self.assertEqual(res.rand_upper_bound, CONST)
        self.assertEqual(res.rand_lower_bound, CONST)

    def test_cycle_path4(self):
        # -undir -n "{ 11, 22, 33 }" -e "{ 12, 21, 13, 31, 23, 32 }"
        # cycle path classifier
        cycle_path_problem4 = GenericProblem(
            ["A A", "B B", "C C"],
            ["A B", "B A", "A C", "C A", "B C", "C B"],
            flags=ProblemFlags(is_cycle=True, is_path=False, is_tree=False),
        )
        res = classify(cycle_path_problem4)
        self.assertEqual(res.det_lower_bound, ITERATED_LOG)
        self.assertEqual(res.det_upper_bound, ITERATED_LOG)
        self.assertEqual(res.rand_upper_bound, ITERATED_LOG)
        self.assertEqual(res.rand_lower_bound, ITERATED_LOG)
