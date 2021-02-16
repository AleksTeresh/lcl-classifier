from typing import NamedTuple, List, Set
from util import onlyOneIsTrue, flatten, letterRange
from functools import reduce
from config_util import parseAndNormalize
import itertools, copy

class ProblemFlags:
  def __init__(
    self,
    isTree: bool = True,
    isCycle: bool = False,
    isPath: bool = False,
    isDirected: bool = False,
    isRooted: bool = False,
    isRegular: bool = True,
  ):
    self.isTree = isTree
    self.isCycle = isCycle
    self.isPath = isPath
    self.isDirected = isDirected
    self.isRooted = isRooted
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
class GenericProblem:
  def  __init__(
    self,
    activeConstraints: List[str],
    passiveConstraints: List[str],
    leafConstraints: List[str] = [],
    rootConstraints: List[str] = [],
    activeAllowAll: bool = False,
    passiveAllowAll: bool = False,
    leafAllowAll: bool = True,
    rootAllowAll: bool = True,
    flags: ProblemFlags = ProblemFlags(),
    id=None
  ):
    self.__checkBadConstrInputs(
      activeConstraints,
      passiveConstraints,
      activeAllowAll,
      passiveAllowAll
    )

    self.__assignActivesAndPassives(
      activeConstraints,
      passiveConstraints,
      activeAllowAll,
      passiveAllowAll
    )

    self.__assumeRootConstr(
      rootAllowAll,
      rootConstraints,
      activeConstraints,
      passiveConstraints
    )

    self.__removeUnusedConfigs()
    
    self.__assignLeafs(leafConstraints, leafAllowAll)
    self.leafAllowAll = leafAllowAll
    
    self.__assignRoots(rootConstraints, rootAllowAll)
    self.rootAllowAll = rootAllowAll
    
    self.flags = flags
    self.id = id

    self.__checkParams()
    self.normalize()

  def __key(self):
    variableDict = copy.deepcopy(self.__dict__)
    if self.id is not None:
      del variableDict['id']
    return tuple(variableDict.values())

  def dict(self):
    return self.__dict__

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
      
    degree = len(list(configs)[0].split(' '))
    isSameDegree = reduce(lambda acc, x: acc and len(x.split(' ')) == degree, configs, True)
    return isSameDegree

  def __checkParams(self):
    if not self.__checkDegrees(self.activeConstraints):
      raise Exception('degree', 'The configurations should be of the same degree', self.activeConstraints)

    if not self.__checkDegrees(self.passiveConstraints):
      raise Exception('degree', 'The configurations should be of the same degree', self.passiveConstraints)

    if not onlyOneIsTrue(self.flags.isTree, self.flags.isCycle, self.flags.isPath):
      raise Exception('graph family', 'Select exactly one option out of "isTree", "isCycle", "isPath"')

    if self.flags.isPath and not self.flags.isDirected and (
      self.leafAllowAll != self.rootAllowAll or self.leafConstraints != self.rootConstraints):
      raise Exception('invalid parameters', 'Leaf and root constraints must be the same on undirected paths') 

  def __checkBadConstrInputs(
    self,
    activeConstraints,
    passiveConstraints,
    activeAllowAll,
    passiveAllowAll
  ):
    if activeAllowAll and passiveAllowAll:
      raise Exception('problem', 'Both activeAllowAll and passiveAllowAll always yield a trivial problem')

    if (not activeConstraints and not activeAllowAll) or (not passiveConstraints and not passiveAllowAll):
      raise Exception('problem', 'If passive or active configuration are empty, the problem is always unsolvable')

    if not activeConstraints:
      raise Exception('problem', 'Specify at least one active config, s.t. the tool knows the degree of active nodes')

    if not passiveConstraints:
      raise Exception('problem', 'Specify at least one passive config, s.t. the tool knows the degree of passive nodes')

  def __assignActivesAndPassives(
    self,
    activeConstraints,
    passiveConstraints,
    activeAllowAll,
    passiveAllowAll
  ):
    self.activeConstraints = tuple(parseAndNormalize(activeConstraints))
    self.passiveConstraints = tuple(parseAndNormalize(passiveConstraints))
    alphabet = self.getAlphabet()

    if activeAllowAll:
      allowAllNotnormnalized = ["".join(alphabet) for _ in activeConstraints[0].split(' ')]
      self.activeConstraints = tuple(parseAndNormalize(allowAllNotnormnalized))

    if passiveAllowAll:
      allowAllNotnormnalized = ["".join(alphabet) for _ in passiveConstraints[0].split(' ')]
      self.passiveConstraints = tuple(parseAndNormalize(allowAllNotnormnalized))

  def __assignLeafs(
    self,
    leafConstraints,
    leafAllowAll
  ):
    self.leafConstraints = tuple(leafConstraints)
    if leafAllowAll:
      allowAllNotnormnalized = ["".join(self.getAlphabet())]
      self.leafConstraints = tuple(parseAndNormalize(allowAllNotnormnalized))

  def __assignRoots(
    self,
    rootConstraints,
    rootAllowAll
  ):
    self.rootConstraints = tuple(rootConstraints)
    if rootAllowAll:
      allowAllNotnormnalized= ["".join(self.getAlphabet())]
      self.rootConstraints = tuple(parseAndNormalize(allowAllNotnormnalized))

  def __assumeRootConstr(
    self,
    rootAllowAll,
    rootConstraints,
    activeConstraints,
    passiveConstraints
  ):
    # if root degree cannot be deduced because rootConstraints is an empty set,
    # assume (rather arbitrarily) that root is an active node
    if rootAllowAll and not rootConstraints:
      rootConstraints = activeConstraints
      alphabet = set(flatten(activeConstraints + passiveConstraints)) - {' '}
      self.rootConstraints = tuple(["".join(alphabet) for _ in rootConstraints[0].split(' ')])

  def __getNewConfig(self, renaming, configuration: str):
    'returns a string of chars'
    newConfig = [renaming[char] for char in configuration]
    # if a graph directed/rooted, the first letter in the config
    # has a special meaning (it is config towards parent/predecessor node)
    # Thus, leave the first letter in the first position. Sort other letters
    if len(newConfig) != 0 and (self.flags.isDirected or self.flags.isRooted):
      newConfig = [newConfig[0]] + sorted(newConfig[1:])
    else:
      newConfig = sorted(newConfig)
    return "".join(newConfig)

  # adopted from https://github.com/olidennis/round-eliminator/blob/fa43fc97f4ac03273211a08d012de4f77f342fe4/simulation/src/constraint.rs#L469-L489
  def __permuteNormalize(self, renaming, constraints: tuple):
    'returns a list of strings'  
    newConfigs = [self.__getNewConfig(renaming, x) for x in constraints]

    newConfigs = list(set(newConfigs)) # i.e. unique()
    newConfigs = sorted(newConfigs)
    return newConfigs

  def __handleAlphabetPerm(self, perm):
    'returns a tuple of lists'
    renaming = {}
        
    for (x, y) in zip(self.getAlphabet(), perm):
      renaming[x] = y

    newActive = self.__permuteNormalize(renaming, self.activeConstraints)
    newPassive = self.__permuteNormalize(renaming, self.passiveConstraints)
    newLeaf = self.__permuteNormalize(renaming, self.leafConstraints)
    newRoot = self.__permuteNormalize(renaming, self.rootConstraints)

    return (newActive, newPassive, newLeaf, newRoot)

  # for now works only for active and passive constraints
  # leaf and root constraints are yet to come
  def __removeUnusedConfigs(self):
    newActiveConstraints = self.activeConstraints
    newPassiveConstraints = self.passiveConstraints

    activeAlphabet = set(flatten(newActiveConstraints)) - {' '}
    passiveAlphabet = set(flatten(newPassiveConstraints)) - {' '}

    while (
      (activeAlphabet - passiveAlphabet) or
      (passiveAlphabet - activeAlphabet)
    ):
      diff = (activeAlphabet - passiveAlphabet)
      if diff:
        newActiveConstraints = [conf for conf in self.activeConstraints if not diff.intersection(set(conf))]

      diff = (passiveAlphabet - activeAlphabet)
      if diff:
        newPassiveConstraints = [conf for conf in self.passiveConstraints if not diff.intersection(set(conf))]

      if not newActiveConstraints or not newPassiveConstraints:
        raise Exception('problem', 'If passive or active configuration are empty, the problem is always unsolvable')

      activeAlphabet = set(flatten(newActiveConstraints)) - {' '}
      passiveAlphabet = set(flatten(newPassiveConstraints)) - {' '}

    self.activeConstraints = tuple(newActiveConstraints)
    self.passiveConstraints = tuple(newPassiveConstraints)

  def getAlphabet(self):
    return set(flatten(self.activeConstraints + self.passiveConstraints)) - {' '}

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

