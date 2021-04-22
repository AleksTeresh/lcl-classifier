from typing import List, Dict, Tuple
from own_types import UnparsedConfigType, ConfigType
from util import only_one_is_true, flatten, letter_range
from .config_util import parse_and_normalize
from .config_util import are_regular
from .config_util import are_some_directed_by_unparsed_configs
from .config_util import are_all_directed_by_unparsed_configs
from .config_util import get_degree_by_unparsed_config
from .config_util import is_regular_by_unparsed_configs
import itertools, copy


class BasicProblemFlags:
    def __init__(
        self,
        is_tree: bool = True,
        is_cycle: bool = False,
        is_path: bool = False,
    ):
        self.is_tree = is_tree
        self.is_cycle = is_cycle
        self.is_path = is_path


class ProblemFlags(BasicProblemFlags):
    def __init__(
        self,
        is_tree: bool = True,
        is_cycle: bool = False,
        is_path: bool = False,
        is_directed_or_rooted: bool = False,
        is_regular: bool = True,
    ):
        BasicProblemFlags.__init__(
            self, is_tree=is_tree, is_cycle=is_cycle, is_path=is_path
        )
        self.is_directed_or_rooted = is_directed_or_rooted
        self.is_regular = is_regular

    def __key(self) -> Tuple:
        return tuple(self.__dict__.values())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.__key())

    def dict(self) -> Dict:
        return self.__dict__


class ProblemProps:
    def __init__(
        self,
        active_degree: int,
        passive_degree: int,
        label_count: int,
        actives_all_same: bool,
        passives_all_same: bool,
        flags: ProblemFlags,
    ):
        self.active_degree = active_degree
        self.passive_degree = passive_degree
        self.label_count = label_count
        self.actives_all_same = actives_all_same
        self.passives_all_same = passives_all_same
        self.flags = flags

        if self.active_degree < self.passive_degree:
            self.__swap_active_passive()

    def __swap_active_passive(self):
        self.active_degree, self.passive_degree = (
            self.passive_degree,
            self.active_degree,
        )
        self.actives_all_same, self.passives_all_same = (
            self.passives_all_same,
            self.actives_all_same,
        )


class GenericProblem:
    def __init__(
        self,
        active_constraints: UnparsedConfigType,
        passive_constraints: UnparsedConfigType,
        leaf_constraints: UnparsedConfigType = [],
        root_constraints: UnparsedConfigType = [],
        active_allow_all: bool = False,
        passive_allow_all: bool = False,
        leaf_allow_all: bool = True,
        root_allow_all: bool = True,
        flags: BasicProblemFlags = BasicProblemFlags(),
        id=None,
    ):
        self.active_constraints = tuple()
        self.passive_constraints = tuple()
        self.root_constraints = tuple()
        self.leaf_constraints = tuple()

        self.__check_bad_constr_inputs(
            active_constraints, passive_constraints, active_allow_all, passive_allow_all
        )

        self.__assign_actives_and_passives(
            active_constraints, passive_constraints, active_allow_all, passive_allow_all
        )

        self.__assume_root_constr(
            root_allow_all, root_constraints, active_constraints, passive_constraints
        )

        self.__assign_leafs(leaf_constraints, leaf_allow_all)
        self.leaf_allow_all = leaf_allow_all

        self.__assign_roots(root_constraints, root_allow_all)
        self.root_allow_all = root_allow_all

        self.__remove_unused_configs()

        self.flags = self.__get_flags(flags, active_constraints, passive_constraints)
        self.id = id

        self.__check_flags()
        self.normalize()

    def __key(self) -> Tuple:
        variable_dict = copy.deepcopy(self.__dict__)
        if self.id is not None:
            del variable_dict["id"]
        return tuple(variable_dict.values())

    def dict(self) -> Dict:
        return {**self.__dict__, "flags": self.flags.dict()}

    def __repr__(self) -> str:
        return self.__dict__.__repr__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        else:
            return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() < other.__key()
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.__key())

    def __get_flags(
        self,
        basic_flags: BasicProblemFlags,
        unparsed_active_constraints: UnparsedConfigType,
        unparsed_passive_constraints: UnparsedConfigType,
    ) -> ProblemFlags:
        is_regular = are_regular(self.active_constraints, self.passive_constraints)
        is_path = basic_flags.is_path or (
            basic_flags.is_tree
            and is_regular
            and get_degree_by_unparsed_config(unparsed_active_constraints[0]) == 2
            and get_degree_by_unparsed_config(unparsed_passive_constraints[0]) == 2
        )
        return ProblemFlags(
            is_tree=basic_flags.is_tree and not is_path,
            is_cycle=basic_flags.is_cycle,
            is_path=is_path,
            is_directed_or_rooted=are_all_directed_by_unparsed_configs(
                unparsed_active_constraints
            ),
            is_regular=is_regular,
        )

    def __check_flags(self) -> None:
        if not only_one_is_true(
            self.flags.is_tree, self.flags.is_cycle, self.flags.is_path
        ):
            raise Exception(
                "problem",
                'Select exactly one option out of "is_tree", "is_cycle", "is_path"',
            )

        if (
            self.flags.is_path
            and not self.flags.is_directed_or_rooted
            and (
                self.leaf_allow_all != self.root_allow_all
                or self.leaf_constraints != self.root_constraints
            )
        ):
            raise Exception(
                "problem",
                "Leaf and root constraints must be the same on undirected paths",
            )

        if (self.flags.is_path or self.flags.is_cycle) and (
            self.get_active_degree() != 2 or self.get_passive_degree() != 2
        ):
            raise Exception(
                "problem",
                "Problems on paths or cycles must have active and passive configs of degree 2",
            )

    def __check_bad_constr_inputs(
        self,
        active_constraints: UnparsedConfigType,
        passive_constraints: UnparsedConfigType,
        active_allow_all: bool,
        passive_allow_all: bool,
    ) -> None:
        if active_allow_all and passive_allow_all:
            raise Exception(
                "problem",
                "Both active_allow_all and passive_allow_all always yield a trivial problem",
            )

        if (not active_constraints and not active_allow_all) or (
            not passive_constraints and not passive_allow_all
        ):
            raise Exception(
                "problem",
                "If passive or active configuration are empty, the problem is always unsolvable",
            )

        if not active_constraints:
            raise Exception(
                "problem",
                "Specify at least one active config, s.t. the tool knows the degree of active nodes",
            )

        if not passive_constraints:
            raise Exception(
                "problem",
                "Specify at least one passive config, s.t. the tool knows the degree of passive nodes",
            )

        some_configs_are_directed = are_some_directed_by_unparsed_configs(
            active_constraints + passive_constraints
        )
        all_configs_are_directed = are_all_directed_by_unparsed_configs(
            active_constraints + passive_constraints
        )
        # if a single constraint is directed, all has to be directed
        if some_configs_are_directed != all_configs_are_directed:
            raise Exception(
                "problem",
                "If a single config is directed, all configs have to be directed",
                active_constraints,
                passive_constraints,
            )

        if not is_regular_by_unparsed_configs(active_constraints):
            raise Exception(
                "problem",
                "Active configurations must be of the same degree",
                active_constraints,
            )

        if not is_regular_by_unparsed_configs(passive_constraints):
            raise Exception(
                "problem",
                "Passive configurations must be of the same degree",
                passive_constraints,
            )

    def __swap_constraints(self) -> None:
        temp = self.active_constraints
        self.active_constraints = self.passive_constraints
        self.passive_constraints = temp

    def __assign_actives_and_passives(
        self,
        active_constraints: UnparsedConfigType,
        passive_constraints: UnparsedConfigType,
        active_allow_all: bool,
        passive_allow_all: bool,
    ) -> None:
        self.active_constraints = parse_and_normalize(active_constraints)
        self.passive_constraints = parse_and_normalize(passive_constraints)
        alphabet = self.get_alphabet()

        if active_allow_all:
            allow_all_notnormnalized = [
                "".join(alphabet) for _ in active_constraints[0].split(" ")
            ]
            self.active_constraints = parse_and_normalize(allow_all_notnormnalized)

        if passive_allow_all:
            allow_all_notnormnalized = [
                "".join(alphabet) for _ in passive_constraints[0].split(" ")
            ]
            self.passive_constraints = parse_and_normalize(allow_all_notnormnalized)

        if self.get_active_degree() < self.get_passive_degree():
            self.__swap_constraints()

    def __assign_leafs(
        self, leaf_constraints: UnparsedConfigType, leaf_allow_all: bool
    ) -> None:
        if leaf_allow_all:
            allow_all_notnormnalized = ["".join(self.get_alphabet())]
            self.leaf_constraints = parse_and_normalize(allow_all_notnormnalized)
        else:
            self.leaf_constraints = parse_and_normalize(leaf_constraints)

    def __assign_roots(
        self, root_constraints: UnparsedConfigType, root_allow_all: bool
    ) -> None:
        if root_allow_all:
            allow_all_notnormnalized = ["".join(self.get_alphabet())]
            self.root_constraints = parse_and_normalize(allow_all_notnormnalized)
        else:
            self.root_constraints = parse_and_normalize(root_constraints)

    def __assume_root_constr(
        self,
        root_allow_all: bool,
        root_constraints: UnparsedConfigType,
        active_constraints: UnparsedConfigType,
        passive_constraints: UnparsedConfigType,
    ) -> None:
        # if root degree cannot be deduced because root_constraints is an empty set,
        # assume (rather arbitrarily) that root is an active node
        if root_allow_all and not root_constraints:
            root_constraints = active_constraints
            alphabet = set(flatten(active_constraints + passive_constraints)) - {" "}
            self.root_constraints = tuple(
                ["".join(alphabet) for _ in root_constraints[0].split(" ")]
            )

    def __get_new_config(self, renaming: Dict[str, str], configuration: str) -> str:
        "returns a string of chars"
        new_config = [renaming[char] for char in configuration]
        # if a graph directed/rooted, the first letter in the config
        # has a special meaning (it is config towards parent/predecessor node)
        # Thus, leave the first letter in the first position. Sort other letters
        if len(new_config) != 0 and (self.flags.is_directed_or_rooted):
            new_config = [new_config[0]] + sorted(new_config[1:])
        else:
            new_config = sorted(new_config)
        return "".join(new_config)

    # adopted from https://github.com/olidennis/round-eliminator/blob/fa43fc97f4ac03273211a08d012de4f77f342fe4/simulation/src/constraint.rs#L469-L489
    def __permute_normalize(
        self, renaming: Dict[str, str], constraints: ConfigType
    ) -> ConfigType:
        "returns a list of strings"
        new_configs = [self.__get_new_config(renaming, x) for x in constraints]

        new_configs = list(set(new_configs))  # i.e. unique()
        new_configs = sorted(new_configs)
        return tuple(new_configs)

    def __handle_alphabet_perm(
        self, perm: Tuple[str, ...]
    ) -> Tuple[ConfigType, ConfigType, ConfigType, ConfigType]:
        "returns a tuple of lists"
        renaming = {}

        for (x, y) in zip(self.get_alphabet(), perm):
            renaming[x] = y

        new_active = self.__permute_normalize(renaming, self.active_constraints)
        new_passive = self.__permute_normalize(renaming, self.passive_constraints)
        new_leaf = self.__permute_normalize(renaming, self.leaf_constraints)
        new_root = self.__permute_normalize(renaming, self.root_constraints)

        return (new_active, new_passive, new_leaf, new_root)

    def __remove_unused_configs(self) -> None:
        new_active_constraints = self.active_constraints
        new_passive_constraints = self.passive_constraints

        active_alphabet = set(flatten(new_active_constraints)) - {" "}
        passive_alphabet = set(flatten(new_passive_constraints)) - {" "}

        while (active_alphabet - passive_alphabet) or (
            passive_alphabet - active_alphabet
        ):
            # print(active_alphabet, passive_alphabet)
            diff = active_alphabet - passive_alphabet
            if diff:
                new_active_constraints = tuple(
                    [
                        conf
                        for conf in new_active_constraints
                        if not diff.intersection(set(conf))
                    ]
                )

            diff = passive_alphabet - active_alphabet
            if diff:
                new_passive_constraints = tuple(
                    [
                        conf
                        for conf in new_passive_constraints
                        if not diff.intersection(set(conf))
                    ]
                )

            if not new_active_constraints:
                raise Exception(
                    "problem",
                    "After removing configs that can never be used, active configurations become empty.",
                )

            if not new_passive_constraints:
                raise Exception(
                    "problem",
                    "After removing configs that can never be used, passive configurations become empty.",
                )

            active_alphabet = set(flatten(new_active_constraints)) - {" "}
            passive_alphabet = set(flatten(new_passive_constraints)) - {" "}

        self.active_constraints = new_active_constraints
        self.passive_constraints = new_passive_constraints

        leaf_alphabet = set(flatten(self.leaf_constraints)) - {" "}
        root_alphabet = set(flatten(self.root_constraints)) - {" "}
        allowed_alphabet = active_alphabet

        leaf_diff = leaf_alphabet - allowed_alphabet
        if leaf_diff:
            self.leaf_constraints = tuple(
                [
                    conf
                    for conf in self.leaf_constraints
                    if not leaf_diff.intersection(set(conf))
                ]
            )

        root_diff = root_alphabet - allowed_alphabet
        if root_diff:
            self.root_constraints = tuple(
                [
                    conf
                    for conf in self.root_constraints
                    if not root_diff.intersection(set(conf))
                ]
            )

    def __get_degree(self, configs: ConfigType) -> int:
        return len(configs[0])

    def get_alphabet(self) -> List[str]:
        return list(
            set(
                flatten(
                    self.active_constraints
                    + self.passive_constraints
                    + self.root_constraints
                    + self.leaf_constraints
                )
            )
            - {" "}
        )

    def get_active_degree(self) -> int:
        return self.__get_degree(self.active_constraints)

    def get_passive_degree(self) -> int:
        return self.__get_degree(self.passive_constraints)

    # adopted from https://github.com/olidennis/round-eliminator/blob/fa43fc97f4ac03273211a08d012de4f77f342fe4/simulation/src/problem.rs#L156-L171
    def normalize(self) -> None:
        label_count = len(self.get_alphabet())
        letters = letter_range(label_count)
        all_perms = list(itertools.permutations(letters))
        normalized = [self.__handle_alphabet_perm(perm) for perm in all_perms]
        # normalized is a list of tulpes of lists
        normalized_first = sorted(normalized)[0]
        self.active_constraints = normalized_first[0]
        self.passive_constraints = normalized_first[1]
        self.leaf_constraints = normalized_first[2]
        self.root_constraints = normalized_first[3]
