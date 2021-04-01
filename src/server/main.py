import sys
from typing import Optional
from problem import ProblemFlags, ProblemProps
from classify import reclassify_and_store
from classify import classify_and_store
from problem import generate
from statistics import compute as compute_stats, pretty_print
from query import Query
from db import store_problems_and_get_with_ids
from db import get_classified_problem_objs
from db import get_batchless_problem_objs


def reclassify_individual_problems():
    problems = get_batchless_problem_objs()
    reclassify_and_store(problems)


def reclassify_problem_class(
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
):
    """
    Reclassify a class of already existing problems that are stored
    in the DB. This is much faster than generating the class of problems all over again and classifying them.
    This is mainly because the generation step takes very long
    for big (even if partial) problem classes
    """
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
        actives_all_same,
        passives_all_same,
        flags=flags,
    )

    query = Query(props)
    responses = get_classified_problem_objs(query)
    ps_with_ids = [r.to_problem() for r in responses]
    classify_and_store(
        ps_with_ids,
        props=props,
        count_limit=count_limit if count_limit is None else len(ps_with_ids),
        skip_count=skip_count,
    )

    res = get_classified_problem_objs(query)
    stats = compute_stats(res)
    pretty_print(stats)


def generate_problem_class(
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
):
    print("Generating the following:")
    print("  active_degree = %s," % active_degree)
    print("  passive_degree = %s," % passive_degree)
    print("  label_count = %s," % label_count)
    print("  is_directed_or_rooted = %s" % is_directed_or_rooted)

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
        actives_all_same,
        passives_all_same,
        flags=flags,
    )

    query = Query(props)

    ps = generate(
        active_degree,
        passive_degree,
        label_count,
        actives_all_same,
        passives_all_same,
        flags,
        count_limit=(sys.maxsize if count_limit is None else count_limit),
        skip_count=(0 if skip_count is None else skip_count),
    )

    ps_with_ids = store_problems_and_get_with_ids(ps, props)
    classify_and_store(
        ps_with_ids,
        props=props,
        count_limit=count_limit if count_limit is None else len(ps),
        skip_count=skip_count,
    )

    res = get_classified_problem_objs(query)
    stats = compute_stats(res)
    pretty_print(stats)


print("Press Enter to start reclassification...")
input()

reclassify_individual_problems()

generate_problem_class(
    active_degree=2,
    passive_degree=2,
    label_count=2,
    is_directed_or_rooted=False,
    is_path=True,
)

generate_problem_class(
    active_degree=2,
    passive_degree=2,
    label_count=2,
    is_directed_or_rooted=False,
    is_cycle=True,
)

generate_problem_class(
    active_degree=2,
    passive_degree=2,
    label_count=2,
    is_directed_or_rooted=True,
    is_path=True,
)

generate_problem_class(
    active_degree=2,
    passive_degree=2,
    label_count=2,
    is_directed_or_rooted=True,
    is_cycle=True,
)

generate_problem_class(
    active_degree=2,
    passive_degree=2,
    label_count=3,
    is_directed_or_rooted=False,
    is_path=True,
)

generate_problem_class(
    active_degree=2,
    passive_degree=2,
    label_count=3,
    is_directed_or_rooted=True,
    is_path=True,
)

generate_problem_class(
    active_degree=2,
    passive_degree=2,
    label_count=4,
    is_directed_or_rooted=False,
    is_path=True,
)

generate_problem_class(
    active_degree=3,
    passive_degree=2,
    label_count=2,
    is_directed_or_rooted=False,
    is_tree=True,
)

generate_problem_class(
    active_degree=3,
    passive_degree=2,
    label_count=2,
    is_directed_or_rooted=True,
    is_tree=True,
)

generate_problem_class(
    active_degree=3,
    passive_degree=2,
    label_count=3,
    is_directed_or_rooted=False,
    is_tree=True,
)

generate_problem_class(
    active_degree=3,
    passive_degree=2,
    label_count=3,
    is_directed_or_rooted=True,
    is_tree=True,
    passives_all_same=True,
)

generate_problem_class(
    active_degree=3,
    passive_degree=2,
    label_count=4,
    is_directed_or_rooted=True,
    is_tree=True,
    actives_all_same=True,
)


generate_problem_class(
    active_degree=2,
    passive_degree=2,
    label_count=4,
    is_directed_or_rooted=True,
    is_path=True,
    count_limit=sys.maxsize,
    skip_count=0,
)

## Example for reclassifying a class of problems
# reclassify_problem_class(
#     active_degree=2,
#     passive_degree=2,
#     label_count=4,
#     is_directed_or_rooted=True,
#     is_path=True,
#     count_limit=sys.maxsize,
#     skip_count=0,
# )

generate_problem_class(
    active_degree=3,
    passive_degree=2,
    label_count=3,
    is_directed_or_rooted=True,
    is_tree=True,
    count_limit=sys.maxsize,
    skip_count=0,
)

generate_problem_class(
    active_degree=3,
    passive_degree=2,
    label_count=4,
    is_directed_or_rooted=True,
    is_tree=True,
    passives_all_same=True,
    count_limit=sys.maxsize,
    skip_count=0,
)

# generate_problem_class(
#     active_degree=3,
#     passive_degree=2,
#     label_count=4,
#     is_directed_or_rooted=False,
#     is_tree=True,
# )
