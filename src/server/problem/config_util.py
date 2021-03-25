from typing import List
from own_types import ConfigType, UnparsedConfigType
from functools import reduce
from itertools import product
from util import flatMap, flatten, areAllTheSame, allSameSizes
from .parser import parseConfigs

def flattenBinaryConfigs(left: List[str], right: List[str]) -> List[str]:
    return [l + r for l in left for r in right]


def flattenTernaryConfigs(one: List[str], two: List[str], three: List[str]) -> List[str]:
    return [o + tw + th for o in one for tw in two for th in three]


def flattenConfigs(configs: List[List[str]]) -> List[str]:
    if len(configs) == 1:
        return flatten(configs)
    elif len(configs) == 2:
        return flattenBinaryConfigs(configs[0], configs[1])
    elif len(configs) == 3:
        return flattenTernaryConfigs(configs[0], configs[1], configs[2])
    else:
        return ["".join(x) for x in product(*configs)]


def normalizeConstraints(constr: List[List[List[str]]]) -> List[str]:
    return flatMap(lambda x: flattenConfigs(x), constr)


def parseAndNormalize(constr: UnparsedConfigType) -> ConfigType:
    constr = parseConfigs(constr)
    constr = [] if not constr else list(normalizeConstraints(constr))
    return tuple(constr)


def eachConstrIsHomogeneous(constrs: ConfigType) -> bool:
    return reduce(lambda acc, x: acc and areAllTheSame(flatten(x)), constrs, True)


def areRegular(activeConfig: ConfigType, passiveConfig: ConfigType) -> bool:
    return allSameSizes(activeConfig) and allSameSizes(passiveConfig)


def isDirectedByUnparsedConfig(unparsedConfig: str) -> bool:
    return ":" in unparsedConfig


def areSomeDirectedByUnparsedConfigs(unparsedConfigs: UnparsedConfigType) -> bool:
    unparsedConfigs = [x for x in unparsedConfigs if x.strip() != ""]
    return reduce(
        lambda acc, x: acc or isDirectedByUnparsedConfig(x), unparsedConfigs, False
    )


def areAllDirectedByUnparsedConfigs(unparsedConfigs: UnparsedConfigType) -> bool:
    unparsedConfigs = [x for x in unparsedConfigs if x.strip() != ""]
    return reduce(
        lambda acc, x: acc and isDirectedByUnparsedConfig(x), unparsedConfigs, True
    )


def getDegreeByUnparsedConfig(unparsedConfig: str) -> int:
    perEdgeConfigs = [x.strip().split(" ") for x in unparsedConfig.strip().split(":")]
    perEdgeConfigs = flatten(perEdgeConfigs)
    perEdgeConfigs = [x for x in perEdgeConfigs if x != ""]
    return len(perEdgeConfigs)


def isRegularByUnparsedConfigs(unparsedConfigs: UnparsedConfigType) -> bool:
    unparsedConfigs = [x for x in unparsedConfigs if x.strip() != ""]
    return areAllTheSame([getDegreeByUnparsedConfig(c) for c in unparsedConfigs])
