from typing import List, Optional
from tqdm import tqdm
from collections import namedtuple
from db import updateClassifications
from db import storeProblemAndClassification
from .classifier import classify, Classifier
from bindings import tlpBatchClassify
from bindings import brtBatchClassify
from problem import GenericProblem, ProblemFlags, ProblemProps
from response import GenericResponse
from db import ClassifiedProblem
from bindings import ClassifyContext


def batchClassify(problems: List[GenericProblem]) -> List[GenericResponse]:
    context = ClassifyContext(isBatch=True)

    try:
        tlpResponses = tlpBatchClassify(problems)
        context.tlpPreclassified = True
    except Exception as e:
        print(e)
        tlpResponses = []

    try:
        brtResponses = brtBatchClassify(problems)
        context.brtPreclassified = True
    except Exception as e:
        print(e)
        brtResponses = []

    return [
        classify(
            x,
            {
                k: v
                for k, v in {
                    Classifier.BRT: (
                        brtResponses[i] if context.brtPreclassified else None
                    ),
                    Classifier.TLP: (
                        tlpResponses[i] if context.tlpPreclassified else None
                    ),
                }.items()
                if v is not None
            },
            context,
        )
        for i, x in enumerate(tqdm(problems))
    ]


def classifyAndStore(
    problems: List[GenericProblem],
    props: ProblemProps,
    countLimit: Optional[int],
    skipCount: Optional[int],
) -> None:
    results = batchClassify(problems)
    updateClassifications(results, props, countLimit, skipCount)


def reclassifyAndStore(classifiedProblems: List[ClassifiedProblem]) -> None:
    for p in tqdm(classifiedProblems):
        res = classify(p.toProblem())
        storeProblemAndClassification(p, res)
