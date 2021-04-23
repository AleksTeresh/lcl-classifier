import sys
from typing import Iterator, List, Tuple
from own_types import ConfigType
from tqdm import tqdm
from util import letter_range, powerset
from .problem import GenericProblem as P, BasicProblemFlags, ProblemFlags
from itertools import combinations_with_replacement, product


def problem_from_constraints(
    tulpes: Iterator[Tuple[ConfigType, ConfigType]],
    flags: ProblemFlags,
) -> List[P]:
    for i, (a, b) in enumerate(tqdm(tulpes)):
        try:
            p = P(
                (
                    a
                    if (not flags.is_directed_or_rooted)
                    else [c.replace(" ", " : ", 1) for c in a]
                ),
                (
                    b
                    if (not flags.is_directed_or_rooted)
                    else [c.replace(" ", " : ", 1) for c in b]
                ),
                flags=BasicProblemFlags(
                    is_tree=flags.is_tree,
                    is_cycle=flags.is_cycle,
                    is_path=flags.is_path,
                ),
                id=i,
            )
        except Exception as e:
            if e.args[0] == "problem":
                continue
            else:
                raise e

        yield p


def generate(
    active_degree: int,
    passive_degree: int,
    label_count: int,
    actives_all_same: bool,
    passives_all_same: bool,
    flags: ProblemFlags,
    count_limit: int = sys.maxsize,  # TODO: remove the param or use it
    skip_count: int = 0,  # TODO: remove the param or use it
) -> List[P]:
    alphabet = letter_range(label_count)
    # take active_degree labels
    # from a pallete of active_label_count
    if flags.is_directed_or_rooted:
        # rooted/directed: order of configs does not matter,
        # except for the frist label in each config. Thus,
        # we have additional product() call below.
        # e.g. degree = 3, labels = 2, gives us:
        # ['AAA', 'AAB', 'ABB', 'BAA', 'BAB', 'BBB']
        actives = (
            "".join(x)
            for x in combinations_with_replacement(alphabet, active_degree - 1)
        )
        passives = (
            "".join(x)
            for x in combinations_with_replacement(alphabet, passive_degree - 1)
        )
        actives = ("".join(x) for x in product(alphabet, actives))
        passives = ("".join(x) for x in product(alphabet, passives))
    else:
        # unrooted/undirected: order of configs does not matter
        # e.g. degree 3, labels = 2, gives us
        # ['AAA', 'AAB', 'ABB', 'BBB']
        actives = (
            "".join(x) for x in combinations_with_replacement(alphabet, active_degree)
        )
        passives = (
            "".join(x) for x in combinations_with_replacement(alphabet, passive_degree)
        )

    if actives_all_same:
        actives = (x for x in actives if x[0] * len(x) == x)
    if passives_all_same:
        passives = (x for x in passives if x[0] * len(x) == x)

    active_constraints = (
        tuple([" ".join(y) for y in x]) for x in tqdm(powerset(actives)) if x
    )
    passive_constraints = (
        tuple([" ".join(y) for y in x]) for x in tqdm(powerset(passives)) if x
    )

    problem_tuples = (
        (a, b) for (a, b) in product(active_constraints, passive_constraints)
    )
    return problem_from_constraints(problem_tuples, flags)
