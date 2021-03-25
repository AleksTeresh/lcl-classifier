from problem import GenericProblem
from response import GenericResponse, Sources
from complexity import complexities
from complexity import *
from classifier_types import *
from bindings import ClassifyContext
from typing import List, Dict, Tuple
from own_types import ComplexityType
from bindings import cpClassify
from bindings import rtClassify
from bindings import tlpClassify
from bindings import brtClassify
from bindings import reClassify


def getUpperBound(
    responses: Dict[str, GenericResponse], attrStr: str
) -> Tuple[Classifier, ComplexityType]:
    classifierToComplexityIdx = {
        k: complexities.index(getattr(res, attrStr)) for k, res in responses.items()
    }
    minClassifier = min(classifierToComplexityIdx, key=classifierToComplexityIdx.get)
    minComplexityIdx = classifierToComplexityIdx[minClassifier]
    return minClassifier, complexities[minComplexityIdx]


def getLowerBound(
    responses: Dict[str, GenericResponse], attrStr: str
) -> Tuple[Classifier, ComplexityType]:
    classifierToComplexityIdx = {
        k: complexities.index(getattr(res, attrStr)) for k, res in responses.items()
    }
    maxClassifier = max(classifierToComplexityIdx, key=classifierToComplexityIdx.get)
    maxComplexityIdx = classifierToComplexityIdx[maxClassifier]
    return maxClassifier, complexities[maxComplexityIdx]


def removeUnknowns(response: GenericResponse) -> GenericResponse:
    if response.randLowerBound == UNKNOWN:
        response.randLowerBound = CONST
    if response.detLowerBound == UNKNOWN:
        response.detLowerBound = CONST
    if response.randUpperBound == UNKNOWN:
        response.randUpperBound = UNSOLVABLE
    if response.detUpperBound == UNKNOWN:
        response.detUpperBound = UNSOLVABLE
    return response


def propagateBounds(response: GenericResponse) -> GenericResponse:
    # propagate rand upper
    if complexities.index(response.detUpperBound) < complexities.index(
        response.randUpperBound
    ):
        response.randUpperBound = response.detUpperBound
        response.papers.randUpperBoundSource = response.papers.detUpperBoundSource

    # propagate det lower
    if complexities.index(response.randLowerBound) > complexities.index(
        response.detLowerBound
    ):
        response.detLowerBound = response.randLowerBound
        response.papers.detLowerBoundSource = response.papers.randLowerBoundSource

    # propagate det upper
    if response.randUpperBound != LOGLOG:
        response.detUpperBound = response.randUpperBound
        response.papers.detUpperBoundSource = response.papers.randUpperBoundSource
    elif complexities.index(LOG) < complexities.index(response.detUpperBound):
        response.detUpperBound = LOG
        # source of detUpperBound is still in this case
        # dictated by randUpperBound
        response.papers.detUpperBoundSource = response.papers.randUpperBoundSource

    # propagate rand lower
    if response.detLowerBound != LOG:
        response.randLowerBound = response.detLowerBound
        response.papers.randLowerBoundSource = response.papers.detLowerBoundSource
    elif complexities.index(LOGLOG) > complexities.index(response.randLowerBound):
        response.randLowerBound = LOGLOG
        # source of randLowerBoundSource is still in this case
        # dictated by detLowerBoundSource
        response.papers.randLowerBoundSource = response.papers.detLowerBoundSource

    return response


def postprocess(response: GenericResponse) -> GenericResponse:
    response = removeUnknowns(response)
    response = propagateBounds(response)
    return response


def checkForContradictions(responses: Dict[str, GenericResponse]) -> None:
    _, randUpperBound = getUpperBound(responses, "randUpperBound")
    _, detUpperBound = getUpperBound(responses, "detUpperBound")
    _, randLowerBound = getLowerBound(responses, "randLowerBound")
    _, detLowerBound = getLowerBound(responses, "detLowerBound")
    for r in responses.values():
        if complexities.index(r.randLowerBound) > complexities.index(randUpperBound):
            raise Exception(
                "classification-contradiction",
                "randLowerBound in one of the respones is > randUpperBound in another response",
                responses,
                r.problem,
            )
        if complexities.index(r.detLowerBound) > complexities.index(detUpperBound):
            raise Exception(
                "classification-contradiction"
                "detLowerBound in one of the respones is > detUpperBound in another response",
                responses,
                r.problem,
            )
        if complexities.index(r.randUpperBound) < complexities.index(randLowerBound):
            raise Exception(
                "classification-contradiction"
                "randUpperBound in one of the respones is < randLowerBound in another response",
                responses,
                r.problem,
            )
        if complexities.index(r.detUpperBound) < complexities.index(detLowerBound):
            raise Exception(
                "classification-contradiction"
                "randUpperBound in one of the respones is < randLowerBound in another response",
                responses,
                r.problem,
            )


def classify(
    problem: GenericProblem,
    existingClassifications: Dict[str, GenericResponse] = {},
    context: ClassifyContext = ClassifyContext(),
) -> GenericResponse:
    try:
        cpResult = cpClassify(problem, context)
    except Exception:
        cpResult = GenericResponse(problem)

    try:
        rtResult = rtClassify(problem, context)
    except Exception:
        rtResult = GenericResponse(problem)

    try:
        tlpResult = tlpClassify(problem, context)
    except Exception:
        tlpResult = GenericResponse(problem)

    try:
        brtResult = brtClassify(problem, context)
    except Exception:
        brtResult = GenericResponse(problem)

    try:
        reResult = reClassify(problem, context)
    except Exception:
        reResult = GenericResponse(problem)

    responses = {
        Classifier.CP: cpResult,
        Classifier.RT: rtResult,
        Classifier.TLP: tlpResult,
        Classifier.BRT: brtResult,
        Classifier.RE: reResult,
        **existingClassifications,
    }

    checkForContradictions(responses)

    rubSource, rub = getUpperBound(responses, "randUpperBound")
    rlbSource, rlb = getLowerBound(responses, "randLowerBound")
    dubSource, dub = getUpperBound(responses, "detUpperBound")
    dlbSource, dlb = getLowerBound(responses, "detLowerBound")

    response = GenericResponse(
        problem,
        rub,
        rlb,
        dub,
        dlb,
        cpResult.solvableCount,
        cpResult.unsolvableCount,
        papers=Sources(
            context.sources[rubSource],
            context.sources[rlbSource],
            context.sources[dubSource],
            context.sources[dlbSource],
        ),
    )

    return postprocess(response)
