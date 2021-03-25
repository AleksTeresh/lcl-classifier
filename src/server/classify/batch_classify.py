from typing import List
from tqdm import tqdm
from collections import namedtuple
from db import updateClassifications
from db import storeProblemAndClassification
from .classifier import classify, Classifier
from bindings import tlpBatchClassify
from bindings import brtBatchClassify
from problem import GenericProblem, ProblemFlags, ProblemProps
from db import ClassifiedProblem
from bindings import ClassifyContext

def batchClassify(problems: List[GenericProblem]):
    context = ClassifyContext(isBatch=True)

    try:
        tlpResponses = tlpBatchClassify(problems)
        context.tlpPreclassified = True
    except Exception as e:
        print(e)
        tlpResponses = []
    except e:
        print(e)

    try:
        brtResponses = brtBatchClassify(problems)
        context.brtPreclassified = True
    except Exception as e:
        print(e)
        brtResponses = []
    except e:
        print(e)

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
    problems: List[GenericProblem], props: ProblemProps, countLimit, skipCount
):
    results = batchClassify(problems)
    updateClassifications(results, props, countLimit, skipCount)


def reclassifyAndStore(classifiedProblems):
    for p in tqdm(classifiedProblems):
        res = classify(p.toProblem())
        storeProblemAndClassification(p, res)
