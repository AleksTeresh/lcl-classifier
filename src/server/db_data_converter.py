from classified_problem import ClassifiedProblem
from response import Sources, Source


def mapToClassifiedProblem(dbProblem) -> ClassifiedProblem:
    return ClassifiedProblem(
        papers=Sources(
            randUpperBoundSource=Source(
                dbProblem["rubSourceShortName"],
                dbProblem["rubSourceName"],
                dbProblem["rubSourceUrls"],
            )
            if dbProblem["rubSourceShortName"] is not None
            else None,
            randLowerBoundSource=Source(
                dbProblem["rlbSourceShortName"],
                dbProblem["rlbSourceName"],
                dbProblem["rlbSourceUrls"],
            )
            if dbProblem["rlbSourceShortName"] is not None
            else None,
            detUpperBoundSource=Source(
                dbProblem["dubSourceShortName"],
                dbProblem["dubSourceName"],
                dbProblem["dubSourceUrls"],
            )
            if dbProblem["dubSourceShortName"] is not None
            else None,
            detLowerBoundSource=Source(
                dbProblem["dlbSourceShortName"],
                dbProblem["dlbSourceName"],
                dbProblem["dlbSourceUrls"],
            )
            if dbProblem["dlbSourceShortName"] is not None
            else None,
        ),
        **dbProblem
    )
