from typing import List
from problem import GenericProblem
from .classify_context import ClassifyContext

from tlp_classifier import (
    get_problem,
    get_problems,
    complexity_name,
    Complexity as tlp_complexity,
)
from response import GenericResponse
from complexity import *

complexity_mapping = {
    tlp_complexity.Constant: CONST,
    tlp_complexity.Iterated_Logarithmic: ITERATED_LOG,
    tlp_complexity.Logarithmic: LOG,
    tlp_complexity.Global: GLOBAL,
    tlp_complexity.Unsolvable: UNSOLVABLE,
    tlp_complexity.Unclassified: UNKNOWN,
}


def validate(p: GenericProblem) -> None:
    if p.flags.is_cycle:
        raise Exception("tlp", "Cannot classify if the graph is a cycle")

    if p.flags.is_directed_or_rooted:
        raise Exception("tlp", "Cannot classify if the tree/path is rooted/directed")

    if not p.flags.is_regular:
        raise Exception("tlp", "Cannot classify if the graph is not regular")

    if not p.root_allow_all or not p.leaf_allow_all:
        raise Exception("tlp", "Leaves and roots must allow all configurations")

    if len(p.get_alphabet()) > 3:
        raise Exception("tlp", "Cannot classify problems with more than 3 labels")

    active_degree = len(p.active_constraints[0]) if len(p.active_constraints) else 3
    passive_degree = len(p.passive_constraints[0]) if len(p.passive_constraints) else 2

    if not (
        (active_degree == 2 and passive_degree == 2)
        or (active_degree == 2 and passive_degree == 3)
        or (active_degree == 3 and passive_degree == 2)
    ):
        raise Exception(
            "rooted-tree", "Allowed degrees pairs are (2, 2), (2, 3), (3, 2)"
        )


def batch_classify(ps: List[GenericProblem]) -> List[GenericResponse]:
    try:
        for p in ps:
            validate(p)
    except Exception as e:
        print(e)
        raise Exception("Cannot batch classify")

    results = get_problems([(p.active_constraints, p.passive_constraints) for p in ps])
    return [
        GenericResponse(
            ps[i],
            complexity_mapping[
                r.upper_bound
            ],  # because deterministic UB is also a randomised UB
            CONST,
            complexity_mapping[r.upper_bound],
            complexity_mapping[r.lower_bound],
        )
        for i, r in enumerate(results)
    ]


def classify(p: GenericProblem, context: ClassifyContext) -> GenericResponse:
    if context.tlp_preclassified:
        return GenericResponse(p)

    validate(p)
    result = get_problem(p.active_constraints, p.passive_constraints)

    return GenericResponse(
        p,
        complexity_mapping[
            result.upper_bound
        ],  # because deterministic UB is also a randomised UB
        CONST,
        complexity_mapping[result.upper_bound],
        complexity_mapping[result.lower_bound],
    )
