from typing import List
from problem import GenericProblem
from .classify_context import ClassifyContext

from tlp_classifier import (
    get_problem,
    get_problems,
    complexity_name,
    Complexity as tlpComplexity,
)
from response import GenericResponse
from complexity import *

complexityMapping = {
    tlpComplexity.Constant: CONST,
    tlpComplexity.Iterated_Logarithmic: ITERATED_LOG,
    tlpComplexity.Logarithmic: LOG,
    tlpComplexity.Global: GLOBAL,
    tlpComplexity.Unsolvable: UNSOLVABLE,
    tlpComplexity.Unclassified: UNKNOWN,
}


def validate(p: GenericProblem):
    if p.flags.isCycle:
        raise Exception("tlp", "Cannot classify if the graph is a cycle")

    if p.flags.isDirectedOrRooted:
        raise Exception("tlp", "Cannot classify if the tree/path is rooted/directed")

    if not p.flags.isRegular:
        raise Exception("tlp", "Cannot classify if the graph is not regular")

    if not p.rootAllowAll or not p.leafAllowAll:
        raise Exception("tlp", "Leaves and roots must allow all configurations")

    if len(p.getAlphabet()) > 3:
        raise Exception("tlp", "Cannot classify problems with more than 3 labels")

    activeDegree = len(p.activeConstraints[0]) if len(p.activeConstraints) else 3
    passiveDegree = len(p.passiveConstraints[0]) if len(p.passiveConstraints) else 2

    if not (
        (activeDegree == 2 and passiveDegree == 2)
        or (activeDegree == 2 and passiveDegree == 3)
        or (activeDegree == 3 and passiveDegree == 2)
    ):
        raise Exception(
            "rooted-tree", "Allowed degrees pairs are (2, 2), (2, 3), (3, 2)"
        )


def batchClassify(ps: List[GenericProblem]):
    try:
        for p in ps:
            validate(p)
    except Exception as e:
        print(e)
        raise Exception("Cannot batch classify")

    results = get_problems([(p.activeConstraints, p.passiveConstraints) for p in ps])
    return [
        GenericResponse(
            ps[i],
            complexityMapping[
                r.upper_bound
            ],  # because deterministic UB is also a randomised UB
            CONST,
            complexityMapping[r.upper_bound],
            complexityMapping[r.lower_bound],
        )
        for i, r in enumerate(results)
    ]


def classify(p: GenericProblem, context: ClassifyContext):
    if context.tlpPreclassified:
        return GenericResponse(p)

    validate(p)
    result = get_problem(p.activeConstraints, p.passiveConstraints)

    return GenericResponse(
        p,
        complexityMapping[
            result.upper_bound
        ],  # because deterministic UB is also a randomised UB
        CONST,
        complexityMapping[result.upper_bound],
        complexityMapping[result.lower_bound],
    )
