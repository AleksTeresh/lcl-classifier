from typing import List
from own_types import ConfigType, UnparsedConfigType
from functools import reduce
from itertools import product
from util import flat_map, flatten, are_all_the_same, all_same_sizes
from .parser import parse_configs


def flatten_binary_configs(left: List[str], right: List[str]) -> List[str]:
    return [l + r for l in left for r in right]


def flatten_ternary_configs(
    one: List[str], two: List[str], three: List[str]
) -> List[str]:
    return [o + tw + th for o in one for tw in two for th in three]


def flatten_configs(configs: List[List[str]]) -> List[str]:
    if len(configs) == 1:
        return flatten(configs)
    elif len(configs) == 2:
        return flatten_binary_configs(configs[0], configs[1])
    elif len(configs) == 3:
        return flatten_ternary_configs(configs[0], configs[1], configs[2])
    else:
        return ["".join(x) for x in product(*configs)]


def normalize_constraints(constr: List[List[List[str]]]) -> List[str]:
    return flat_map(lambda x: flatten_configs(x), constr)


def parse_and_normalize(constr: UnparsedConfigType) -> ConfigType:
    parsed_constr = parse_configs(constr)
    normalized_constr = (
        [] if not parsed_constr else list(normalize_constraints(parsed_constr))
    )
    return tuple(normalized_constr)


def each_constr_is_homogeneous(constrs: ConfigType) -> bool:
    return reduce(lambda acc, x: acc and are_all_the_same(flatten(x)), constrs, True)


def are_regular(active_config: ConfigType, passive_config: ConfigType) -> bool:
    return all_same_sizes(active_config) and all_same_sizes(passive_config)


def is_directed_by_unparsed_config(unparsed_config: str) -> bool:
    return ":" in unparsed_config


def are_some_directed_by_unparsed_configs(unparsed_configs: UnparsedConfigType) -> bool:
    unparsed_configs = [x for x in unparsed_configs if x.strip() != ""]
    return reduce(
        lambda acc, x: acc or is_directed_by_unparsed_config(x), unparsed_configs, False
    )


def are_all_directed_by_unparsed_configs(unparsed_configs: UnparsedConfigType) -> bool:
    unparsed_configs = [x for x in unparsed_configs if x.strip() != ""]
    return reduce(
        lambda acc, x: acc and is_directed_by_unparsed_config(x), unparsed_configs, True
    )


def get_degree_by_unparsed_config(unparsed_config: str) -> int:
    per_edge_configs = [
        x.strip().split(" ") for x in unparsed_config.strip().split(":")
    ]
    per_edge_configs = flatten(per_edge_configs)
    per_edge_configs = [x for x in per_edge_configs if x != ""]
    return len(per_edge_configs)


def is_regular_by_unparsed_configs(unparsed_configs: UnparsedConfigType) -> bool:
    unparsed_configs = [x for x in unparsed_configs if x.strip() != ""]
    return are_all_the_same(
        [get_degree_by_unparsed_config(c) for c in unparsed_configs]
    )
