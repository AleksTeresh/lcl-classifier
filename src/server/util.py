from typing import Sequence, List, Tuple
from itertools import chain, combinations
from functools import reduce

flat_map = lambda f, arr: list(reduce(lambda a, b: a + b, map(f, arr)))

flatten = lambda arr: flat_map(lambda x: x, arr)


def only_one_is_true(a: bool, b: bool, c: bool) -> bool:
    return (a and not b and not c) or (not a and b and not c) or (not a and not b and c)


def are_all_the_same(list: Sequence) -> bool:
    return len(list) == 0 or list.count(list[0]) == len(list)


def all_same_sizes(list: Sequence[Sequence]) -> bool:
    return are_all_the_same([len(x) for x in list])


def powerset(iterable: Sequence) -> List[Tuple]:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def letter_range(count: int) -> List[str]:
    nums = list(range(count))
    letters = [chr(x + 65) for x in nums]  # TODO: works only when num_labels < 27
    return letters
