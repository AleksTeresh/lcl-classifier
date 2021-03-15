from typing import NamedTuple, List, Set
from util import onlyOneIsTrue, flatten, letterRange
from functools import reduce
from config_util import parseAndNormalize
from config_util import areRegular
from config_util import isDirectedByUnparsedConfigs
from config_util import getDegreeByUnparsedConfig
from config_util import isRegularByUnparsedConfigs
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

    def __key(self):
        return tuple(self.__dict__.values())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        else:
            return False

    def __hash__(self):
        return hash(self.__key())

    def dict(self):
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
        activeConstraints: List[str],
        passiveConstraints: List[str],
        leafConstraints: List[str] = [],
        rootConstraints: List[str] = [],
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

    def __key(self):
        variableDict = copy.deepcopy(self.__dict__)
        if self.id is not None:
            del variableDict["id"]
        return tuple(variableDict.values())

    def dict(self):
        return {**self.__dict__, "flags": self.flags.dict()}

    def __repr__(self):
        return self.__dict__.__repr__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        else:
            return False

    def __hash__(self):
        return hash(self.__key())

    def __checkDegrees(self, configs):
        if len(configs) == 0:
            return configs

        degree = self.__getDegree(configs)
        isSameDegree = reduce(lambda acc, x: acc and len(x) == degree, configs, True)
        return isSameDegree

    def __getFlags(
        self,
        basicFlags: BasicProblemFlags,
        unparsedActiveConstraints: List[str],
        unparsedPassiveConstraints: List[str],
    ):
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
            isDirectedOrRooted=isDirectedByUnparsedConfigs(unparsedActiveConstraints),
            isRegular=isRegular,
        )

    def __checkFlags(self):
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
        self, activeConstraints, passiveConstraints, activeAllowAll, passiveAllowAll
    ):
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

        directedConfig = isDirectedByUnparsedConfigs(
            activeConstraints + passiveConstraints
        )
        # if a single constraint is directed, all has to be directed
        for c in activeConstraints + passiveConstraints:
            if (":" in c) != directedConfig:
                raise Exception(
                    "problem",
                    "If a single config is directed, all configs has to be directed",
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

    def __swapConstraints(self):
        temp = self.activeConstraints
        self.activeConstraints = self.passiveConstraints
        self.passiveConstraints = temp

    def __assignActivesAndPassives(
        self, activeConstraints, passiveConstraints, activeAllowAll, passiveAllowAll
    ):
        self.activeConstraints = tuple(parseAndNormalize(activeConstraints))
        self.passiveConstraints = tuple(parseAndNormalize(passiveConstraints))
        alphabet = self.getAlphabet()

        if activeAllowAll:
            allowAllNotnormnalized = [
                "".join(alphabet) for _ in activeConstraints[0].split(" ")
            ]
            self.activeConstraints = tuple(parseAndNormalize(allowAllNotnormnalized))

        if passiveAllowAll:
            allowAllNotnormnalized = [
                "".join(alphabet) for _ in passiveConstraints[0].split(" ")
            ]
            self.passiveConstraints = tuple(parseAndNormalize(allowAllNotnormnalized))

        if self.getActiveDegree() < self.getPassiveDegree():
            self.__swapConstraints()

    def __assignLeafs(self, leafConstraints, leafAllowAll):
        self.leafConstraints = tuple(leafConstraints)
        if leafAllowAll:
            allowAllNotnormnalized = ["".join(self.getAlphabet())]
            self.leafConstraints = tuple(parseAndNormalize(allowAllNotnormnalized))

    def __assignRoots(self, rootConstraints, rootAllowAll):
        self.rootConstraints = tuple(rootConstraints)
        if rootAllowAll:
            allowAllNotnormnalized = ["".join(self.getAlphabet())]
            self.rootConstraints = tuple(parseAndNormalize(allowAllNotnormnalized))

    def __assumeRootConstr(
        self, rootAllowAll, rootConstraints, activeConstraints, passiveConstraints
    ):
        # if root degree cannot be deduced because rootConstraints is an empty set,
        # assume (rather arbitrarily) that root is an active node
        if rootAllowAll and not rootConstraints:
            rootConstraints = activeConstraints
            alphabet = set(flatten(activeConstraints + passiveConstraints)) - {" "}
            self.rootConstraints = tuple(
                ["".join(alphabet) for _ in rootConstraints[0].split(" ")]
            )

    def __getNewConfig(self, renaming, configuration: str):
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
    def __permuteNormalize(self, renaming, constraints: tuple):
        "returns a list of strings"
        newConfigs = [self.__getNewConfig(renaming, x) for x in constraints]

        newConfigs = list(set(newConfigs))  # i.e. unique()
        newConfigs = sorted(newConfigs)
        return newConfigs

    def __handleAlphabetPerm(self, perm):
        "returns a tuple of lists"
        renaming = {}

        for (x, y) in zip(self.getAlphabet(), perm):
            renaming[x] = y

        newActive = self.__permuteNormalize(renaming, self.activeConstraints)
        newPassive = self.__permuteNormalize(renaming, self.passiveConstraints)
        newLeaf = self.__permuteNormalize(renaming, self.leafConstraints)
        newRoot = self.__permuteNormalize(renaming, self.rootConstraints)

        return (newActive, newPassive, newLeaf, newRoot)

    def __removeUnusedConfigs(self):
        newActiveConstraints = self.activeConstraints
        newPassiveConstraints = self.passiveConstraints

        activeAlphabet = set(flatten(newActiveConstraints)) - {" "}
        passiveAlphabet = set(flatten(newPassiveConstraints)) - {" "}

        while (activeAlphabet - passiveAlphabet) or (passiveAlphabet - activeAlphabet):
            # print(activeAlphabet, passiveAlphabet)
            diff = activeAlphabet - passiveAlphabet
            if diff:
                newActiveConstraints = [
                    conf
                    for conf in newActiveConstraints
                    if not diff.intersection(set(conf))
                ]

            diff = passiveAlphabet - activeAlphabet
            if diff:
                newPassiveConstraints = [
                    conf
                    for conf in newPassiveConstraints
                    if not diff.intersection(set(conf))
                ]

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

        self.activeConstraints = tuple(newActiveConstraints)
        self.passiveConstraints = tuple(newPassiveConstraints)

        leafAlphabet = set(flatten(self.leafConstraints)) - {" "}
        rootAlphabet = set(flatten(self.rootConstraints)) - {" "}
        allowedAlphabet = activeAlphabet

        leafDiff = leafAlphabet - allowedAlphabet
        if leafDiff:
            self.leafConstraints = [
                conf
                for conf in self.leafConstraints
                if not leafDiff.intersection(set(conf))
            ]

        rootDiff = rootAlphabet - allowedAlphabet
        if rootDiff:
            self.rootConstraints = [
                conf
                for conf in self.rootConstraints
                if not rootDiff.intersection(set(conf))
            ]

    def __getDegree(self, configs):
        return len(configs[0])

    def getAlphabet(self):
        return set(flatten(self.activeConstraints + self.passiveConstraints)) - {" "}

    def getActiveDegree(self):
        return self.__getDegree(self.activeConstraints)

    def getPassiveDegree(self):
        return self.__getDegree(self.passiveConstraints)

    # adopted from https://github.com/olidennis/round-eliminator/blob/fa43fc97f4ac03273211a08d012de4f77f342fe4/simulation/src/problem.rs#L156-L171
    def normalize(self):
        labelCount = len(self.getAlphabet())
        letters = letterRange(labelCount)
        allPerms = list(itertools.permutations(letters))
        normalized = [self.__handleAlphabetPerm(perm) for perm in allPerms]
        # normalized is a list of tulpes of lists
        normalized = sorted(normalized)[0]
        self.activeConstraints = tuple(normalized[0])
        self.passiveConstraints = tuple(normalized[1])
        self.leafConstraints = tuple(normalized[2])
        self.rootConstraints = tuple(normalized[3])
