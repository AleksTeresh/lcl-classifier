from rooted_tree_classifier import (
    is_log_star_solvable,
    is_log_solvable,
    is_constant_solvable,
)
from problem import GenericProblem
from problem import each_constr_is_homogeneous
from response import GenericResponse
from .classify_context import ClassifyContext
from complexity import *
from .common import move_root_label_to_center


def classify(p: GenericProblem, context: ClassifyContext) -> GenericResponse:
    if not p.flags.is_tree:
        raise Exception("rooted-tree", "Cannot classify if the problem is not a tree")

    if not p.flags.is_directed_or_rooted:
        raise Exception("rooted-tree", "Cannot classify if the tree is not rooted")

    if not p.flags.is_regular:
        raise Exception("rooted-tree", "Cannot classify if the graph is not regular")

    if not p.root_allow_all or not p.leaf_allow_all:
        raise Exception("rooted-tree", "Leaves and roots must allow all configurations")

    active_degree = len(p.active_constraints[0]) if len(p.active_constraints) else 3
    passive_degree = len(p.passive_constraints[0]) if len(p.passive_constraints) else 2

    if active_degree != 3:
        raise Exception("rooted-tree", "Active configurations must be of size 3")

    if passive_degree != 2:
        raise Exception("rooted-tree", "Passive configurations must be of size 2")

    if not each_constr_is_homogeneous(p.passive_constraints):
        raise Exception(
            "rooted-tree",
            "Passive constraints must be simple pairs of the same labels.",
        )

    constraints = [move_root_label_to_center(x) for x in p.active_constraints]

    det_upper_bound = UNSOLVABLE
    det_lower_bound = CONST
    rand_upper_bound = UNSOLVABLE
    rand_lower_bound = CONST
    if is_log_solvable(constraints):  # is not empty
        if is_log_star_solvable(constraints):
            if is_constant_solvable(constraints):
                det_upper_bound = CONST
                rand_upper_bound = CONST
            else:
                det_upper_bound = ITERATED_LOG
                det_lower_bound = ITERATED_LOG
                rand_upper_bound = ITERATED_LOG
                rand_lower_bound = ITERATED_LOG
        else:
            det_upper_bound = LOG
            det_lower_bound = LOG
            rand_upper_bound = LOG
            rand_lower_bound = LOG  # because LOGLOG does not exist in the setting
    else:
        det_lower_bound = GLOBAL
        rand_lower_bound = GLOBAL

    return GenericResponse(
        p, rand_upper_bound, rand_lower_bound, det_upper_bound, det_lower_bound
    )
