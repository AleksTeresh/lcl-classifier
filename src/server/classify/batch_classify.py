from typing import List, Optional
from tqdm import tqdm
from db import update_classifications
from db import store_problem_and_classification
from .classifier import classify, Classifier
from bindings import tlp_batch_classify
from bindings import brt_batch_classify
from problem import GenericProblem, ProblemProps
from response import GenericResponse
from db import ClassifiedProblem
from bindings import ClassifyContext


def batch_classify(problems: List[GenericProblem]) -> List[GenericResponse]:
    context = ClassifyContext(is_batch=True)

    try:
        tlp_responses = tlp_batch_classify(problems)
        context.tlp_preclassified = True
    except Exception as e:
        print(e)
        tlp_responses = []

    try:
        brt_responses = brt_batch_classify(problems)
        context.brt_preclassified = True
    except Exception as e:
        print(e)
        brt_responses = []

    return [
        classify(
            x,
            {
                k: v
                for k, v in {
                    Classifier.BRT: (
                        brt_responses[i] if context.brt_preclassified else None
                    ),
                    Classifier.TLP: (
                        tlp_responses[i] if context.tlp_preclassified else None
                    ),
                }.items()
                if v is not None
            },
            context,
        )
        for i, x in enumerate(tqdm(problems))
    ]


def classify_and_store(
    problems: List[GenericProblem],
    props: ProblemProps,
    count_limit: Optional[int],
    skip_count: Optional[int],
) -> None:
    results = batch_classify(problems)
    update_classifications(results, props, count_limit, skip_count)


def reclassify_and_store(classified_problems: List[ClassifiedProblem]) -> None:
    for p in tqdm(classified_problems):
        res = classify(p.to_problem())
        store_problem_and_classification(p, res)
