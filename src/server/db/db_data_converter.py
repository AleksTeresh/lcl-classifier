from typing import Dict
from .classified_problem import ClassifiedProblem
from response import Sources, Source


def map_to_classified_problem(db_problem: Dict) -> ClassifiedProblem:
    return ClassifiedProblem(
        papers=Sources(
            rand_upper_bound_source=Source(
                db_problem["rub_source_short_name"],
                db_problem["rub_source_name"],
                db_problem["rub_source_urls"],
            )
            if db_problem["rub_source_short_name"] is not None
            else None,
            rand_lower_bound_source=Source(
                db_problem["rlb_source_short_name"],
                db_problem["rlb_source_name"],
                db_problem["rlb_source_urls"],
            )
            if db_problem["rlb_source_short_name"] is not None
            else None,
            det_upper_bound_source=Source(
                db_problem["dub_source_short_name"],
                db_problem["dub_source_name"],
                db_problem["dub_source_urls"],
            )
            if db_problem["dub_source_short_name"] is not None
            else None,
            det_lower_bound_source=Source(
                db_problem["dlb_source_short_name"],
                db_problem["dlb_source_name"],
                db_problem["dlb_source_urls"],
            )
            if db_problem["dlb_source_short_name"] is not None
            else None,
        ),
        **db_problem
    )
