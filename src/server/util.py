from typing import Iterable, List, Tuple
from itertools import chain, combinations
from functools import reduce

flatMap = lambda f, arr: list(reduce(lambda a, b: a + b, map(f, arr)))

flatten = lambda arr: flatMap(lambda x: x, arr)


def onlyOneIsTrue(a: bool, b: bool, c: bool) -> bool:
    return (a and not b and not c) or (not a and b and not c) or (not a and not b and c)


def areAllTheSame(list: List) -> bool:
    return len(list) == 0 or list.count(list[0]) == len(list)


def allSameSizes(list: List[Iterable]) -> bool:
    return areAllTheSame([len(x) for x in list])


def powerset(iterable: Iterable) -> List[Tuple]:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def letterRange(count: int) -> List[str]:
    nums = list(range(count))
    letters = [chr(x + 65) for x in nums]  # TODO: works only when numLabels < 27
    return letters
