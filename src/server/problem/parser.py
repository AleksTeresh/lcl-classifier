from own_types import UnparsedConfigType, ConfigType
from typing import List
from util import flat_map, flatten


def split_config(config: str) -> List[str]:
    res = flatten([x.split(" ") for x in config.split(" : ")])
    return [x for x in res if x.strip() != ""]


def valid_labels_from_edge(edge_config: str) -> List[str]:
    half_bracket_split = edge_config.split("(")
    half_bracket_split = [half_bracket_split[0]] + [
        "(" + x for x in half_bracket_split[1:]
    ]
    half_bracket_split = [x for x in half_bracket_split if len(x) > 0]

    full_bracket_split = flat_map(
        lambda x: [y for y in x.split(")") if len(y) > 0], half_bracket_split
    )
    full_bracket_split = [(x + ")") if x[0] == "(" else x for x in full_bracket_split]

    return flat_map(lambda x: [x] if x[0] == "(" else list(x), full_bracket_split)


def parse_config(config: str) -> List[List[str]]:
    config = config.strip()
    per_edge = split_config(config)
    labels_per_edge = [valid_labels_from_edge(x) for x in per_edge]

    return labels_per_edge


def parse_configs(configs: UnparsedConfigType) -> List[List[List[str]]]:
    configs = [x for x in configs if x.strip() != ""]
    return [parse_config(config) for config in configs]


def unparse_config(config: str, is_directed_or_rooted: bool) -> str:
    if is_directed_or_rooted and len(config) > 1:
        config = config[0] + ":" + config[1:]
    return " ".join(config)


def unparse_configs(
    configs: ConfigType, is_directed_or_rooted: bool
) -> UnparsedConfigType:
    return [unparse_config(config, is_directed_or_rooted) for config in configs]
