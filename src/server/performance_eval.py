import timeit
import gc
from typing import List, Optional
from classify import classify as cl
from problem import ProblemFlags, ProblemProps, GenericProblem
from query import Query
from db import get_classified_problem_objs


def get_problem_class(
    active_degree: int,
    passive_degree: int,
    label_count: int,
    is_directed_or_rooted: bool,
    actives_all_same: bool = False,
    passives_all_same: bool = False,
    is_tree: bool = False,
    is_cycle: bool = False,
    is_path: bool = False,
    count_limit: Optional[int] = None,
    skip_count: Optional[int] = None,
) -> List[GenericProblem]:
    flags = ProblemFlags(
        is_tree=is_tree,
        is_cycle=is_cycle,
        is_path=is_path,
        is_directed_or_rooted=is_directed_or_rooted,
    )
    props = ProblemProps(
        active_degree,
        passive_degree,
        label_count,
        actives_all_same=actives_all_same,
        passives_all_same=passives_all_same,
        flags=flags,
    )
    query = Query(props)

    return [p.to_problem() for p in get_classified_problem_objs(query)]


def measure_classify(problems: List[GenericProblem], repeats: int = 1) -> None:
    print("Classifying %s problems" % len(problems))
    maxVal = -1
    for p in problems:
        r = timeit.timeit(
            "cl(p)", "gc.enable()", number=repeats, globals={"p": p, "cl": cl, "gc": gc}
        )
        maxVal = max(maxVal, r / repeats)
        print(r / repeats)
    print("The max classification time was %s" % maxVal)


def measure_problem_query(
    active_degree: int,
    passive_degree: int,
    label_count: int,
    is_directed_or_rooted: bool,
    actives_all_same: bool = False,
    passives_all_same: bool = False,
    is_tree: bool = False,
    is_cycle: bool = False,
    is_path: bool = False,
) -> None:
    flags = ProblemFlags(
        is_tree=is_tree,
        is_cycle=is_cycle,
        is_path=is_path,
        is_directed_or_rooted=is_directed_or_rooted,
    )
    props = ProblemProps(
        active_degree,
        passive_degree,
        label_count,
        actives_all_same=actives_all_same,
        passives_all_same=passives_all_same,
        flags=flags,
    )
    query = Query(props)

    repeats = 1
    r = timeit.timeit(
        "get_classified_problem_objs(query)",
        "gc.enable()",
        number=repeats,
        globals={
            "query": query,
            "get_classified_problem_objs": get_classified_problem_objs,
            "gc": gc,
        },
    )
    print("Query fetch time was %s" % (r / repeats))


# problems = get_problem_class(
#     active_degree=2,
#     passive_degree=2,
#     label_count=2,
#     is_directed_or_rooted=False,
#     is_path=True,
# )
# measure_classify(problems)
# measure_problem_query(
#     active_degree=2,
#     passive_degree=2,
#     label_count=2,
#     is_directed_or_rooted=False,
#     is_path=True,
# )


# problems = get_problem_class(
#     active_degree=3,
#     passive_degree=2,
#     label_count=3,
#     is_directed_or_rooted=True,
#     is_tree=True,
#     passives_all_same=True
# )
# measure_classify(problems)
# measure_problem_query(
#     active_degree=3,
#     passive_degree=2,
#     label_count=3,
#     is_directed_or_rooted=True,
#     is_tree=True,
#     passives_all_same=True
# )
# measure_problem_query(
#     active_degree=3,
#     passive_degree=2,
#     label_count=3,
#     is_directed_or_rooted=True,
#     is_tree=True,
# )

# problems = get_problem_class(
#     active_degree=3,
#     passive_degree=2,
#     label_count=3,
#     is_directed_or_rooted=False,
#     is_tree=True,
#     actives_all_same=True
# )
# measure_classify(problems)
# measure_problem_query(
#     active_degree=3,
#     passive_degree=2,
#     label_count=3,
#     is_directed_or_rooted=False,
#     is_tree=True
# )

measure_problem_query(
    active_degree=2,
    passive_degree=2,
    label_count=3,
    is_directed_or_rooted=True,
    is_path=True,
)
