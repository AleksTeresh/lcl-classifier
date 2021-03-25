from typing import NamedTuple, List, Set, Dict, Tuple
from own_types import UnparsedConfigType, ConfigType
from util import onlyOneIsTrue, flatten, letterRange
from functools import reduce
from .config_util import parseAndNormalize
from .config_util import areRegular
from .config_util import areSomeDirectedByUnparsedConfigs
from .config_util import areAllDirectedByUnparsedConfigs
from .config_util import getDegreeByUnparsedConfig
from .config_util import isRegularByUnparsedConfigs
import itertools, copy


class BasicProblemFlags:
    def __init__(
        self,
        isTree: bool = True,
        isCycle: bool = False,
        isPath: bool = False,
    ):
        self.isTree = isTree
        self.isCycle = isCycle
        self.isPath = isPath


class ProblemFlags(BasicProblemFlags):
    def __init__(
        self,
        isTree: bool = True,
        isCycle: bool = False,
        isPath: bool = False,
        isDirectedOrRooted: bool = False,
        isRegular: bool = True,
    ):
        BasicProblemFlags.__init__(self, isTree=isTree, isCycle=isCycle, isPath=isPath)
        self.isDirectedOrRooted = isDirectedOrRooted
        self.isRegular = isRegular

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
        activeDegree: int,
        passiveDegree: int,
        labelCount: int,
        activesAllSame: bool,
        passivesAllSame: bool,
        flags: ProblemFlags,
    ):
        self.activeDegree = activeDegree
        self.passiveDegree = passiveDegree
        self.labelCount = labelCount
        self.activesAllSame = activesAllSame
        self.passivesAllSame = passivesAllSame
        self.flags = flags


class GenericProblem:
    def __init__(
        self,
        activeConstraints: UnparsedConfigType,
        passiveConstraints: UnparsedConfigType,
        leafConstraints: UnparsedConfigType = [],
        rootConstraints: UnparsedConfigType = [],
        activeAllowAll: bool = False,
        passiveAllowAll: bool = False,
        leafAllowAll: bool = True,
        rootAllowAll: bool = True,
        flags: BasicProblemFlags = BasicProblemFlags(),
        id=None,
    ):
        self.__checkBadConstrInputs(
            activeConstraints, passiveConstraints, activeAllowAll, passiveAllowAll
        )

        self.__assignActivesAndPassives(
            activeConstraints, passiveConstraints, activeAllowAll, passiveAllowAll
        )

        self.__assumeRootConstr(
            rootAllowAll, rootConstraints, activeConstraints, passiveConstraints
        )

        self.__assignLeafs(leafConstraints, leafAllowAll)
        self.leafAllowAll = leafAllowAll

        self.__assignRoots(rootConstraints, rootAllowAll)
        self.rootAllowAll = rootAllowAll

        self.__removeUnusedConfigs()

        self.flags = self.__getFlags(flags, activeConstraints, passiveConstraints)
        self.id = id

        self.__checkFlags()
        self.normalize()

    def __key(self) -> Tuple:
        variableDict = copy.deepcopy(self.__dict__)
        if self.id is not None:
            del variableDict["id"]
        return tuple(variableDict.values())

    def dict(self) -> Dict:
        return {**self.__dict__, "flags": self.flags.dict()}

    def __repr__(self) -> str:
        return self.__dict__.__repr__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.__key())

    def __getFlags(
        self,
        basicFlags: BasicProblemFlags,
        unparsedActiveConstraints: UnparsedConfigType,
        unparsedPassiveConstraints: UnparsedConfigType,
    ) -> ProblemFlags:
        isRegular = areRegular(self.activeConstraints, self.passiveConstraints)
        isPath = basicFlags.isPath or (
            basicFlags.isTree
            and isRegular
            and getDegreeByUnparsedConfig(unparsedActiveConstraints[0]) == 2
            and getDegreeByUnparsedConfig(unparsedPassiveConstraints[0]) == 2
        )
        return ProblemFlags(
            isTree=basicFlags.isTree and not isPath,
            isCycle=basicFlags.isCycle,
            isPath=isPath,
            isDirectedOrRooted=areAllDirectedByUnparsedConfigs(
                unparsedActiveConstraints
            ),
            isRegular=isRegular,
        )

    def __checkFlags(self) -> None:
        if not onlyOneIsTrue(self.flags.isTree, self.flags.isCycle, self.flags.isPath):
            raise Exception(
                "problem",
                'Select exactly one option out of "isTree", "isCycle", "isPath"',
            )

        if (
            self.flags.isPath
            and not self.flags.isDirectedOrRooted
            and (
                self.leafAllowAll != self.rootAllowAll
                or self.leafConstraints != self.rootConstraints
            )
        ):
            raise Exception(
                "problem",
                "Leaf and root constraints must be the same on undirected paths",
            )

        if (self.flags.isPath or self.flags.isCycle) and (
            self.getActiveDegree() != 2 or self.getPassiveDegree() != 2
        ):
            raise Exception(
                "problem",
                "Problems on paths or cycles must have active and passive configs of degree 2",
            )

    def __checkBadConstrInputs(
        self,
        activeConstraints: UnparsedConfigType,
        passiveConstraints: UnparsedConfigType,
        activeAllowAll: bool,
        passiveAllowAll: bool,
    ) -> None:
        if activeAllowAll and passiveAllowAll:
            raise Exception(
                "problem",
                "Both activeAllowAll and passiveAllowAll always yield a trivial problem",
            )

        if (not activeConstraints and not activeAllowAll) or (
            not passiveConstraints and not passiveAllowAll
        ):
            raise Exception(
                "problem",
                "If passive or active configuration are empty, the problem is always unsolvable",
            )

        if not activeConstraints:
            raise Exception(
                "problem",
                "Specify at least one active config, s.t. the tool knows the degree of active nodes",
            )

        if not passiveConstraints:
            raise Exception(
                "problem",
                "Specify at least one passive config, s.t. the tool knows the degree of passive nodes",
            )

        someConfigsAreDirected = areSomeDirectedByUnparsedConfigs(
            activeConstraints + passiveConstraints
        )
        allConfigsAreDirected = areAllDirectedByUnparsedConfigs(
            activeConstraints + passiveConstraints
        )
        # if a single constraint is directed, all has to be directed
        if someConfigsAreDirected != allConfigsAreDirected:
            raise Exception(
                "problem",
                "If a single config is directed, all configs have to be directed",
                activeConstraints,
                passiveConstraints,
            )

        if not isRegularByUnparsedConfigs(activeConstraints):
            raise Exception(
                "problem",
                "Active configurations must be of the same degree",
                activeConstraints,
            )

        if not isRegularByUnparsedConfigs(passiveConstraints):
            raise Exception(
                "problem",
                "Passive configurations must be of the same degree",
                passiveConstraints,
            )

    def __swapConstraints(self) -> None:
        temp = self.activeConstraints
        self.activeConstraints = self.passiveConstraints
        self.passiveConstraints = temp

    def __assignActivesAndPassives(
        self,
        activeConstraints: UnparsedConfigType,
        passiveConstraints: UnparsedConfigType,
        activeAllowAll: bool,
        passiveAllowAll: bool,
    ) -> None:
        self.activeConstraints = parseAndNormalize(activeConstraints)
        self.passiveConstraints = parseAndNormalize(passiveConstraints)
        alphabet = self.getAlphabet()

        if activeAllowAll:
            allowAllNotnormnalized = [
                "".join(alphabet) for _ in activeConstraints[0].split(" ")
            ]
            self.activeConstraints = parseAndNormalize(allowAllNotnormnalized)

        if passiveAllowAll:
            allowAllNotnormnalized = [
                "".join(alphabet) for _ in passiveConstraints[0].split(" ")
            ]
            self.passiveConstraints = parseAndNormalize(allowAllNotnormnalized)

        if self.getActiveDegree() < self.getPassiveDegree():
            self.__swapConstraints()

    def __assignLeafs(
        self, leafConstraints: UnparsedConfigType, leafAllowAll: bool
    ) -> None:
        if leafAllowAll:
            allowAllNotnormnalized = ["".join(self.getAlphabet())]
            self.leafConstraints = parseAndNormalize(allowAllNotnormnalized)
        else:
            self.leafConstraints = parseAndNormalize(leafConstraints)

    def __assignRoots(
        self, rootConstraints: UnparsedConfigType, rootAllowAll: bool
    ) -> None:
        if rootAllowAll:
            allowAllNotnormnalized = ["".join(self.getAlphabet())]
            self.rootConstraints = parseAndNormalize(allowAllNotnormnalized)
        else:
            self.rootConstraints = parseAndNormalize(rootConstraints)

    def __assumeRootConstr(
        self,
        rootAllowAll: bool,
        rootConstraints: UnparsedConfigType,
        activeConstraints: UnparsedConfigType,
        passiveConstraints: UnparsedConfigType,
    ) -> None:
        # if root degree cannot be deduced because rootConstraints is an empty set,
        # assume (rather arbitrarily) that root is an active node
        if rootAllowAll and not rootConstraints:
            rootConstraints = activeConstraints
            alphabet = set(flatten(activeConstraints + passiveConstraints)) - {" "}
            self.rootConstraints = tuple(
                ["".join(alphabet) for _ in rootConstraints[0].split(" ")]
            )

    def __getNewConfig(self, renaming: Dict[str, str], configuration: str) -> str:
        "returns a string of chars"
        newConfig = [renaming[char] for char in configuration]
        # if a graph directed/rooted, the first letter in the config
        # has a special meaning (it is config towards parent/predecessor node)
        # Thus, leave the first letter in the first position. Sort other letters
        if len(newConfig) != 0 and (self.flags.isDirectedOrRooted):
            newConfig = [newConfig[0]] + sorted(newConfig[1:])
        else:
            newConfig = sorted(newConfig)
        return "".join(newConfig)

    # adopted from https://github.com/olidennis/round-eliminator/blob/fa43fc97f4ac03273211a08d012de4f77f342fe4/simulation/src/constraint.rs#L469-L489
    def __permuteNormalize(
        self, renaming: Dict[str, str], constraints: ConfigType
    ) -> ConfigType:
        "returns a list of strings"
        newConfigs = [self.__getNewConfig(renaming, x) for x in constraints]

        newConfigs = list(set(newConfigs))  # i.e. unique()
        newConfigs = sorted(newConfigs)
        return tuple(newConfigs)

    def __handleAlphabetPerm(
        self, perm: Tuple[str, ...]
    ) -> Tuple[ConfigType, ConfigType, ConfigType, ConfigType]:
        "returns a tuple of lists"
        renaming = {}

        for (x, y) in zip(self.getAlphabet(), perm):
            renaming[x] = y

        newActive = self.__permuteNormalize(renaming, self.activeConstraints)
        newPassive = self.__permuteNormalize(renaming, self.passiveConstraints)
        newLeaf = self.__permuteNormalize(renaming, self.leafConstraints)
        newRoot = self.__permuteNormalize(renaming, self.rootConstraints)

        return (newActive, newPassive, newLeaf, newRoot)

    def __removeUnusedConfigs(self) -> None:
        newActiveConstraints = self.activeConstraints
        newPassiveConstraints = self.passiveConstraints

        activeAlphabet = set(flatten(newActiveConstraints)) - {" "}
        passiveAlphabet = set(flatten(newPassiveConstraints)) - {" "}

        while (activeAlphabet - passiveAlphabet) or (passiveAlphabet - activeAlphabet):
            # print(activeAlphabet, passiveAlphabet)
            diff = activeAlphabet - passiveAlphabet
            if diff:
                newActiveConstraints = tuple(
                    [
                        conf
                        for conf in newActiveConstraints
                        if not diff.intersection(set(conf))
                    ]
                )

            diff = passiveAlphabet - activeAlphabet
            if diff:
                newPassiveConstraints = tuple(
                    [
                        conf
                        for conf in newPassiveConstraints
                        if not diff.intersection(set(conf))
                    ]
                )

            if not newActiveConstraints:
                raise Exception(
                    "problem",
                    "After removing configs that can never be used, active configurations become empty.",
                )

            if not newPassiveConstraints:
                raise Exception(
                    "problem",
                    "After removing configs that can never be used, passive configurations become empty.",
                )

            activeAlphabet = set(flatten(newActiveConstraints)) - {" "}
            passiveAlphabet = set(flatten(newPassiveConstraints)) - {" "}

        self.activeConstraints = newActiveConstraints
        self.passiveConstraints = newPassiveConstraints

        leafAlphabet = set(flatten(self.leafConstraints)) - {" "}
        rootAlphabet = set(flatten(self.rootConstraints)) - {" "}
        allowedAlphabet = activeAlphabet

        leafDiff = leafAlphabet - allowedAlphabet
        if leafDiff:
            self.leafConstraints = tuple(
                [
                    conf
                    for conf in self.leafConstraints
                    if not leafDiff.intersection(set(conf))
                ]
            )

        rootDiff = rootAlphabet - allowedAlphabet
        if rootDiff:
            self.rootConstraints = tuple(
                [
                    conf
                    for conf in self.rootConstraints
                    if not rootDiff.intersection(set(conf))
                ]
            )

    def __getDegree(self, configs: ConfigType) -> int:
        return len(configs[0])

    def getAlphabet(self) -> List[str]:
        return list(
            set(flatten(self.activeConstraints + self.passiveConstraints)) - {" "}
        )

    def getActiveDegree(self) -> int:
        return self.__getDegree(self.activeConstraints)

    def getPassiveDegree(self) -> int:
        return self.__getDegree(self.passiveConstraints)

    # adopted from https://github.com/olidennis/round-eliminator/blob/fa43fc97f4ac03273211a08d012de4f77f342fe4/simulation/src/problem.rs#L156-L171
    def normalize(self) -> None:
        labelCount = len(self.getAlphabet())
        letters = letterRange(labelCount)
        allPerms = list(itertools.permutations(letters))
        normalized = [self.__handleAlphabetPerm(perm) for perm in allPerms]
        # normalized is a list of tulpes of lists
        normalizedFirst = sorted(normalized)[0]
        self.activeConstraints = normalizedFirst[0]
        self.passiveConstraints = normalizedFirst[1]
        self.leafConstraints = normalizedFirst[2]
        self.rootConstraints = normalizedFirst[3]
