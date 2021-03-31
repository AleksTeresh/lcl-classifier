from typing import List
from brt_classifier import getProblem, getProblems
from brt_classifier import CONST as BRT_CONST
from brt_classifier import ITERATED_LOG as BRT_ITERATED_LOG
from brt_classifier import LOGLOG as BRT_LOGLOG
from brt_classifier import LOG as BRT_LOG
from brt_classifier import GLOBAL as BRT_GLOBAL
from brt_classifier import UNSOLVABLE as BRT_UNSOLVABLE
from brt_classifier import UNKNOWN as BRT_UNKNOWN
from problem import GenericProblem
from problem import each_constr_is_homogeneous
from .common import move_root_label_to_center
from util import flatten
from .classify_context import ClassifyContext
from response import GenericResponse
from complexity import CONST, ITERATED_LOG, UNKNOWN
from complexity import LOGLOG, LOG, GLOBAL, UNSOLVABLE

complexity_mapping = {
    BRT_CONST: CONST,
    BRT_ITERATED_LOG: ITERATED_LOG,
    BRT_LOGLOG: LOGLOG,
    BRT_LOG: LOG,
    BRT_GLOBAL: GLOBAL,
    BRT_UNSOLVABLE: UNSOLVABLE,
    BRT_UNKNOWN: UNKNOWN,
}


def preprocess_problem(p: GenericProblem) -> List[str]:
    alphabet = p.get_alphabet()
    constraints = [move_root_label_to_center(x) for x in p.active_constraints]

    for i, label in enumerate(alphabet):
        constraints = [x.replace(label, str(i + 1)) for x in constraints]
    return constraints


def validate(p: GenericProblem) -> None:
    if not p.flags.is_tree:
        raise Exception("brt", "Cannot classify if the problem is not a tree")

    if not p.flags.is_directed_or_rooted:
        raise Exception("brt", "Cannot classify if the tree is not rooted")

    if not p.flags.is_regular:
        raise Exception("brt", "Cannot classify if the graph is not regular")

    if not p.root_allow_all or not p.leaf_allow_all:
        raise Exception("brt", "Leaves and roots must allow all configurations")

    active_degree = len(p.active_constraints[0]) if len(p.active_constraints) else 3
    passive_degree = len(p.passive_constraints[0]) if len(p.passive_constraints) else 2

    if active_degree != 3:
        raise Exception("brt", "Active configurations must be of size 3")

    if passive_degree != 2:
        raise Exception("brt", "Passive configurations must be of size 2")

    if not each_constr_is_homogeneous(p.passive_constraints):
        raise Exception(
            "brt", "Passive constraints must be simple pairs of the same labels."
        )


def batch_classify(ps: List[GenericProblem]) -> List[GenericResponse]:
    try:
        for p in ps:
            validate(p)
    except Exception as e:
        print(e)
        raise Exception("Cannot batch classify")

    constrs = [preprocess_problem(p) for p in ps]

    results = getProblems(constrs, len(set(flatten(flatten(constrs)))))

    return [
        GenericResponse(
            ps[i],
            complexity_mapping[r["upper-bound"]],
            complexity_mapping[r["lower-bound"]],
            UNSOLVABLE,
            complexity_mapping[
                r["lower-bound"]
            ],  # because randomised LB is also a deterministic LB
            r["solvable-count"],
            r["unsolvable-count"],
        )
        for i, r in enumerate(results)
    ]


def classify(p: GenericProblem, context: ClassifyContext) -> GenericResponse:
    if context.brt_preclassified:
        return GenericResponse(p)

    validate(p)
    alphabet = p.get_alphabet()
    constraints = [move_root_label_to_center(x) for x in p.active_constraints]

    for i, label in enumerate(alphabet):
        constraints = [x.replace(label, str(i + 1)) for x in constraints]

    result = getProblem(constraints)

    return GenericResponse(
        p,
        complexity_mapping[result["upper-bound"]],
        complexity_mapping[result["lower-bound"]],
        UNSOLVABLE,
        complexity_mapping[
            result["lower-bound"]
        ],  # because randomised LB is also a deterministic LB
        result["solvable-count"],
        result["unsolvable-count"],
    )
