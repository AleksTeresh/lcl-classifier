from own_types import UnparsedConfigType, ConfigType
from typing import List
from util import flatMap, flatten


def splitConfig(config: str) -> List[str]:
    res = flatten([x.split(" ") for x in config.split(" : ")])
    return [x for x in res if x.strip() != ""]


def validLabelsFromEdge(edgeConfig: str) -> List[str]:
    halfBracketSplit = edgeConfig.split("(")
    halfBracketSplit = [halfBracketSplit[0]] + ["(" + x for x in halfBracketSplit[1:]]
    halfBracketSplit = [x for x in halfBracketSplit if len(x) > 0]

    fullBracketSplit = flatMap(
        lambda x: [y for y in x.split(")") if len(y) > 0], halfBracketSplit
    )
    fullBracketSplit = [(x + ")") if x[0] == "(" else x for x in fullBracketSplit]

    return flatMap(lambda x: [x] if x[0] == "(" else list(x), fullBracketSplit)


def parseConfig(config: str) -> List[List[str]]:
    config = config.strip()
    perEdge = splitConfig(config)
    degree = len(perEdge)
    labelsPerEdge = [validLabelsFromEdge(x) for x in perEdge]

    return labelsPerEdge


def parseConfigs(configs: UnparsedConfigType) -> List[List[List[str]]]:
    configs = [x for x in configs if x.strip() != ""]
    return [parseConfig(config) for config in configs]


def unparseConfig(config: str, isDirectedOrRooted: bool) -> str:
    if isDirectedOrRooted and len(config) > 1:
        config = config[0] + ":" + config[1:]
    return " ".join(config)


def unparseConfigs(configs: ConfigType, isDirectedOrRooted: bool) -> UnparsedConfigType:
    return [unparseConfig(config, isDirectedOrRooted) for config in configs]
