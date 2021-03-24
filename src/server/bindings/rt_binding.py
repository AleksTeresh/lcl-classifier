from rooted_tree_classifier import (
    is_log_star_solvable,
    is_log_solvable,
    is_constant_solvable,
)
from problem.problem import GenericProblem
from problem.config_util import eachConstrIsHomogeneous, normalizeConstraints
from response import GenericResponse
from classify.classifier import ClassifyContext
from complexity import *
from .common import moveRootLabelToCenter


def classify(p: GenericProblem, context: ClassifyContext) -> GenericResponse:
    if not p.flags.isTree:
        raise Exception("rooted-tree", "Cannot classify if the problem is not a tree")

    if not p.flags.isDirectedOrRooted:
        raise Exception("rooted-tree", "Cannot classify if the tree is not rooted")

    if not p.flags.isRegular:
        raise Exception("rooted-tree", "Cannot classify if the graph is not regular")

    if not p.rootAllowAll or not p.leafAllowAll:
        raise Exception("rooted-tree", "Leaves and roots must allow all configurations")

    activeDegree = len(p.activeConstraints[0]) if len(p.activeConstraints) else 3
    passiveDegree = len(p.passiveConstraints[0]) if len(p.passiveConstraints) else 2

    if activeDegree != 3:
        raise Exception("rooted-tree", "Active configurations must be of size 3")

    if passiveDegree != 2:
        raise Exception("rooted-tree", "Passive configurations must be of size 2")

    if not eachConstrIsHomogeneous(p.passiveConstraints):
        raise Exception(
            "rooted-tree",
            "Passive constraints must be simple pairs of the same labels.",
        )

    constraints = [moveRootLabelToCenter(x) for x in p.activeConstraints]

    detUpperBound = UNSOLVABLE
    detLowerBound = CONST
    randUpperBound = UNSOLVABLE
    randLowerBound = CONST
    if is_log_solvable(constraints):  # is not empty
        if is_log_star_solvable(constraints):
            if is_constant_solvable(constraints):
                detUpperBound = CONST
                randUpperBound = CONST
            else:
                detUpperBound = ITERATED_LOG
                detLowerBound = ITERATED_LOG
                randUpperBound = ITERATED_LOG
                randLowerBound = ITERATED_LOG
        else:
            detUpperBound = LOG
            detLowerBound = LOG
            randUpperBound = LOG
            randLowerBound = LOG  # because LOGLOG does not exist in the setting
    else:
        detLowerBound = GLOBAL
        randLowerBound = GLOBAL

    return GenericResponse(
        p, randUpperBound, randLowerBound, detUpperBound, detLowerBound
    )
