from classified_problem import ClassifiedProblem
from response import Sources, Source

def mapToClassifiedProblem(dbProblem):
  return ClassifiedProblem(
    papers = Sources(
      randUpperBoundSource = Source(
        dbProblem.rubSourceShortName,
        dbProblem.rubSourceName,
        dbProblem.rubSourceUrls,
      ),
      randLowerBoundSource = Source(
        dbProblem.rlbSourceShortName,
        dbProblem.rlbSourceName,
        dbProblem.rlbSourceUrls,
      ),
      detUpperBoundSource = Source(
        dbProblem.dubSourceShortName,
        dbProblem.dubSourceName,
        dbProblem.dubSourceUrls,
      ),
      detLowerBoundSource = Source(
        dbProblem.dlbSourceShortName,
        dbProblem.dlbSourceName,
        dbProblem.dlbSourceUrls,
      )
    ),
    **dbProblem
  )
