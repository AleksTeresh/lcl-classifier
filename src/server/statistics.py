from complexity import *
import json
from tqdm import tqdm
from typing import NamedTuple, List
from problem import ProblemFlags, ProblemProps
from query import Query
from db import ClassifiedProblem
from db import get_problems


class ComplexityClassData:
    def __init__(
        self,
        rand_lower_bound: int = 0,
        det_lower_bound: int = 0,
        rand_upper_bound: int = 0,
        det_upper_bound: int = 0,
        rand_solvable: int = 0,
        det_solvable: int = 0,
    ):
        self.rand_lower_bound = rand_lower_bound
        self.det_lower_bound = det_lower_bound
        self.rand_upper_bound = rand_upper_bound
        self.det_upper_bound = det_upper_bound

        self.rand_solvable = rand_solvable
        self.det_solvable = det_solvable

    def dict(self):
        return self.__dict__


class StatisticsData:
    def __init__(self):
        self.const: ComplexityClassData = ComplexityClassData()
        self.log_star: ComplexityClassData = ComplexityClassData()
        self.log_log: ComplexityClassData = ComplexityClassData()
        self.log: ComplexityClassData = ComplexityClassData()
        self.linear: ComplexityClassData = ComplexityClassData()
        self.unsolvable: ComplexityClassData = ComplexityClassData()
        self.total_size: int = 0

    def dict(self):
        d = self.__dict__
        for key in d:
            if key != "total_size":
                d[key] = d[key].dict()
        return d


def compute(data: List[ClassifiedProblem]) -> StatisticsData:
    stats = StatisticsData()
    complexity_map = {
        CONST: "const",
        ITERATED_LOG: "log_star",
        LOGLOG: "log_log",
        LOG: "log",
        GLOBAL: "linear",
        UNSOLVABLE: "unsolvable",
    }

    for p in tqdm(data):
        rand_lower_bound = p.rand_lower_bound
        rand_upper_bound = p.rand_upper_bound
        det_lower_bound = p.det_lower_bound
        det_upper_bound = p.det_upper_bound

        cl = complexity_map[rand_lower_bound]
        cu = complexity_map[rand_upper_bound]
        getattr(stats, cl).rand_lower_bound += 1
        getattr(stats, cu).rand_upper_bound += 1
        if cl == cu:
            getattr(stats, cu).rand_solvable += 1

        cl = complexity_map[det_lower_bound]
        cu = complexity_map[det_upper_bound]
        getattr(stats, cl).det_lower_bound += 1
        getattr(stats, cu).det_upper_bound += 1
        if cl == cu:
            getattr(stats, cu).det_solvable += 1

    stats.total_size = len(data)
    return stats


def pretty_print(stats: StatisticsData) -> None:
    print("In total: %s problems" % stats.total_size)
    print()

    print("Stats for randomised setting:")
    print("*****************************")
    print()
    print("Solvable in constant time: %s " % stats.const.rand_solvable)
    print("Solvable in log* time: %s " % stats.log_star.rand_solvable)
    print("Solvable in loglog time: %s " % stats.log_log.rand_solvable)
    print("Solvable in log time: %s " % stats.log.rand_solvable)
    print("Solvable in linear time: %s " % stats.linear.rand_solvable)
    print("Unsolvable: %s" % stats.unsolvable.rand_solvable)
    print(
        "TBD: %s"
        % (
            stats.total_size
            - stats.const.rand_solvable
            - stats.log_star.rand_solvable
            - stats.log_log.rand_solvable
            - stats.log.rand_solvable
            - stats.linear.rand_solvable
            - stats.unsolvable.rand_solvable
        )
    )
    print()

    print("Lower bounds:")
    print("Constant time: %s " % stats.const.rand_lower_bound)
    print("Log* time: %s " % stats.log_star.rand_lower_bound)
    print("Loglog time: %s " % stats.log_log.rand_lower_bound)
    print("Log time: %s " % stats.log.rand_lower_bound)
    print("Linear time: %s " % stats.linear.rand_lower_bound)
    print("Unsolvable: %s" % stats.unsolvable.rand_lower_bound)
    print(
        "TBD: %s"
        % (
            stats.total_size
            - stats.const.rand_lower_bound
            - stats.log_star.rand_lower_bound
            - stats.log_log.rand_lower_bound
            - stats.log.rand_lower_bound
            - stats.linear.rand_lower_bound
            - stats.unsolvable.rand_lower_bound
        )
    )
    print()

    print("Upper bounds:")
    print("Constant time: %s " % stats.const.rand_upper_bound)
    print("Log* time: %s " % stats.log_star.rand_upper_bound)
    print("Loglog time: %s " % stats.log_log.rand_upper_bound)
    print("Log time: %s " % stats.log.rand_upper_bound)
    print("Linear time: %s " % stats.linear.rand_upper_bound)
    print("Unsolvable: %s" % stats.unsolvable.rand_upper_bound)
    print(
        "TBD: %s"
        % (
            stats.total_size
            - stats.const.rand_upper_bound
            - stats.log_star.rand_upper_bound
            - stats.log_log.rand_upper_bound
            - stats.log.rand_upper_bound
            - stats.linear.rand_upper_bound
            - stats.unsolvable.rand_upper_bound
        )
    )
    print()

    print("Stats for deterministic setting:")
    print("*****************************")
    print()
    print("Solvable in constant time: %s " % stats.const.det_solvable)
    print("Solvable in log* time: %s " % stats.log_star.det_solvable)
    print("Solvable in loglog time: %s " % stats.log_log.det_solvable)
    print("Solvable in log time: %s " % stats.log.det_solvable)
    print("Solvable in linear time: %s " % stats.linear.det_solvable)
    print("Unsolvable: %s" % stats.unsolvable.det_solvable)
    print(
        "TBD: %s"
        % (
            stats.total_size
            - stats.const.det_solvable
            - stats.log_star.det_solvable
            - stats.log_log.det_solvable
            - stats.log.det_solvable
            - stats.linear.det_solvable
            - stats.unsolvable.det_solvable
        )
    )
    print()

    print("Lower bounds:")
    print("Constant time: %s " % stats.const.det_lower_bound)
    print("Log* time: %s " % stats.log_star.det_lower_bound)
    print("Loglog time: %s " % stats.log_log.det_lower_bound)
    print("Log time: %s " % stats.log.det_lower_bound)
    print("Linear time: %s " % stats.linear.det_lower_bound)
    print("Unsolvable: %s" % stats.unsolvable.det_lower_bound)
    print(
        "TBD: %s"
        % (
            stats.total_size
            - stats.const.det_lower_bound
            - stats.log_star.det_lower_bound
            - stats.log_log.det_lower_bound
            - stats.log.det_lower_bound
            - stats.linear.det_lower_bound
            - stats.unsolvable.det_lower_bound
        )
    )
    print()

    print("Upper bounds:")
    print("Constant time: %s " % stats.const.det_upper_bound)
    print("Log* time: %s " % stats.log_star.det_upper_bound)
    print("Loglog time: %s " % stats.log_log.det_upper_bound)
    print("Log time: %s " % stats.log.det_upper_bound)
    print("Linear time: %s " % stats.linear.det_upper_bound)
    print("Unsolvable: %s" % stats.unsolvable.det_upper_bound)
    print(
        "TBD: %s"
        % (
            stats.total_size
            - stats.const.det_upper_bound
            - stats.log_star.det_upper_bound
            - stats.log_log.det_upper_bound
            - stats.log.det_upper_bound
            - stats.linear.det_upper_bound
            - stats.unsolvable.det_upper_bound
        )
    )
    print()
