from functools import reduce
from itertools import product
from util import flatMap, flatten, areAllTheSame, allSameSizes
from .parser import parseConfigs


def flattenBinaryConfigs(left, right):
    return [l + r for l in left for r in right]


def flattenTernaryConfigs(one, two, three):
    return [o + tw + th for o in one for tw in two for th in three]


def flattenConfigs(configs):
    if len(configs) == 1:
        return flatten(configs)
    elif len(configs) == 2:
        return flattenBinaryConfigs(configs[0], configs[1])
    elif len(configs) == 3:
        return flattenTernaryConfigs(configs[0], configs[1], configs[2])
    else:
        return ["".join(x) for x in product(*configs)]


def normalizeConstraints(constr):
    return flatMap(lambda x: flattenConfigs(x), constr)


def parseAndNormalize(constr):
    constr = parseConfigs(constr)
    constr = [] if not constr else list(normalizeConstraints(constr))
    return constr


def eachConstrIsHomogeneous(constrs):
    return reduce(lambda acc, x: acc and areAllTheSame(flatten(x)), constrs, True)


def areRegular(activeConfig, passiveConfig):
    return allSameSizes(activeConfig) and allSameSizes(passiveConfig)


def isDirectedByUnparsedConfig(unparsedConfig):
    return ":" in unparsedConfig


def areSomeDirectedByUnparsedConfigs(unparsedConfigs):
    unparsedConfigs = [x for x in unparsedConfigs if x.strip() != ""]
    return reduce(
        lambda acc, x: acc or isDirectedByUnparsedConfig(x), unparsedConfigs, False
    )


def areAllDirectedByUnparsedConfigs(unparsedConfigs):
    unparsedConfigs = [x for x in unparsedConfigs if x.strip() != ""]
    return reduce(
        lambda acc, x: acc and isDirectedByUnparsedConfig(x), unparsedConfigs, True
    )


def getDegreeByUnparsedConfig(unparsedConfig):
    perEdgeConfigs = [x.strip().split(" ") for x in unparsedConfig.strip().split(":")]
    perEdgeConfigs = flatten(perEdgeConfigs)
    perEdgeConfigs = [x for x in perEdgeConfigs if x != ""]
    return len(perEdgeConfigs)


def isRegularByUnparsedConfigs(unparsedConfigs):
    unparsedConfigs = [x for x in unparsedConfigs if x.strip() != ""]
    return areAllTheSame([getDegreeByUnparsedConfig(c) for c in unparsedConfigs])
