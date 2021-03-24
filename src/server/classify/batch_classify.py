from typing import List
from tqdm import tqdm
from collections import namedtuple
from db.db import updateClassifications
from db.db import storeProblemAndClassification
from classify.classifier import classify, Classifier
from bindings.tlp_binding import batchClassify as tlpBatchClassify
from bindings.brt_binding import batchClassify as brtBatchClassify
from problem.problem import GenericProblem, ProblemFlags, ProblemProps
from db.classified_problem import ClassifiedProblem
from classify.classify_context import ClassifyContext


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
