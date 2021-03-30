from problem import GenericProblem
from .classify_context import ClassifyContext
from cyclepath_classifier import classify as cpClassify
from cyclepath_classifier import Problem as CyclePathProblem
from cyclepath_classifier import Type
from cyclepath_classifier import HARD
from cyclepath_classifier import CONST as CP_CONST
from cyclepath_classifier import GLOBAL as CP_GLOBAL
from cyclepath_classifier import ITERATED_LOG as CP_ITERATED_LOG
from cyclepath_classifier import UNSOLVABLE as CP_UNSOLVABLE
from problem import each_constr_is_homogeneous
from util import flatten
from response import GenericResponse
from complexity import *


def classify(p: GenericProblem, context: ClassifyContext) -> GenericResponse:
    active_degree = len(p.active_constraints[0]) if len(p.active_constraints) else 2
    passive_degree = len(p.passive_constraints[0]) if len(p.passive_constraints) else 2
    leaf_degree = len(p.leaf_constraints[0]) if len(p.leaf_constraints) else 1

    if leaf_degree != 1:
        raise Exception("cyclepath", "Leaf constraints must always be of degree 1")

    if passive_degree != 2:
        raise Exception("cyclepath", "Passive constraints must always be of degree 2")

    if p.flags.is_tree:
        if not each_constr_is_homogeneous(p.active_constraints):
            raise Exception(
                "cyclepath",
                "On trees, node constraints must be the same for all incident edges.",
            )
        if not p.flags.is_directed_or_rooted:
            raise Exception(
                "cyclepath",
                "In the context of trees, only rooted ones can be classified.",
            )
    elif active_degree != 2:
        raise Exception(
            "cyclepath",
            "In a path or cycle, active constraints must always be of degree 2",
        )

    problem_type = (
        Type.TREE
        if p.flags.is_tree
        else (Type.DIRECTED if p.flags.is_directed_or_rooted else Type.UNDIRECTED)
    )

    if not p.flags.is_directed_or_rooted:
        p.passive_constraints = p.passive_constraints + tuple(
            [cs[::-1] for cs in p.passive_constraints]
        )
        p.active_constraints = p.active_constraints + tuple(
            [cs[::-1] for cs in p.active_constraints]
        )

    edge_constraints = set(p.passive_constraints)
    node_constraints = {} if problem_type == Type.TREE else set(p.active_constraints)
    start_constraints = {} if p.root_allow_all else set(p.root_constraints)
    end_constraints = {} if p.leaf_allow_all else set(p.leaf_constraints)

    cp_problem = CyclePathProblem(
        node_constraints,
        edge_constraints,
        start_constraints,
        end_constraints,
        problem_type,
    )

    result = cpClassify(cp_problem)

    complexity_mapping = {
        CP_CONST: CONST,
        CP_GLOBAL: GLOBAL,
        CP_ITERATED_LOG: ITERATED_LOG,
        CP_UNSOLVABLE: UNSOLVABLE,
    }
    normalised_complexity = complexity_mapping[result["complexity"]]

    return GenericResponse(
        p,
        normalised_complexity,
        normalised_complexity,
        normalised_complexity,
        normalised_complexity,
        result["solvable"],
        result["unsolvable"],
    )
