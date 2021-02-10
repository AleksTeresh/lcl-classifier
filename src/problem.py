from typing import NamedTuple, List, Set
from util import onlyOneIsTrue, flatten
from functools import reduce
from parser import parseConfigs
from config_util import normalizeConstraints
import itertools

class GenericProblem:
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

    if not onlyOneIsTrue(self.isTree, self.isCycle, self.isPath):
      raise Exception('graph family', 'Select exactly one option out of "isTree", "isCycle", "isPath"')

    if self.isPath and not self.isDirected and (
      self.leafAllowAll != self.rootAllowAll or self.leafConstraints != self.rootConstraints):
      raise Exception('invalid parameters', 'Leaf and root constraints must be the same on undirected paths') 

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
    isTree: bool = True,
    isCycle: bool = False,
    isPath: bool = False,
    isDirected: bool = False,
    isRooted: bool = False,
    isRegular: bool = True,
  ):
    if activeAllowAll and passiveAllowAll:
      raise Exception('problem', 'Both activeAllowAll and passiveAllowAll always yield a trivial problem')

    if (not activeConstraints and not activeAllowAll) or (not passiveConstraints and not passiveAllowAll):
      raise Exception('problem', 'If passive or active configuration are empty, the problem is always unsolvable')

    if not activeConstraints:
      raise Exception('problem', 'Specify at least one active config, s.t. the tool knows the degree of active nodes')

    if not passiveConstraints:
      raise Exception('problem', 'Specify at least one passive config, s.t. the tool knows the degree of passive nodes')

    # if root degree cannot be deduced because rootConstraints is an empty set,
    # assume (rather arbitrarily) that root is an active node
    if rootAllowAll and not rootConstraints:
      rootConstraints = activeConstraints

    alphabet = set(flatten(activeConstraints + passiveConstraints)) - {' '}

    self.activeConstraints = activeConstraints
    if activeAllowAll:
      self.activeConstraints = ["".join(alphabet) for _ in activeConstraints[0].split(' ')]
    # self.activeAllowAll = activeAllowAll
    
    self.passiveConstraints = passiveConstraints
    if passiveAllowAll:
      self.passiveConstraints = ["".join(alphabet) for _ in passiveConstraints[0].split(' ')]
    # self.passiveAllowAll = passiveAllowAll
    
    self.leafConstraints = leafConstraints
    if leafAllowAll:
      self.leafConstraints = ["".join(alphabet)]
    self.leafAllowAll = leafAllowAll
    
    self.rootConstraints = rootConstraints
    if rootAllowAll:
      self.rootConstraints = ["".join(alphabet) for _ in rootConstraints[0].split(' ')]
    self.rootAllowAll = rootAllowAll
    
    self.isCycle = isCycle
    self.isPath = isPath
    self.isDirected = isDirected

    self.isTree = isTree
    self.isRooted = isRooted

    self.isRegular = isRegular

    self.__checkParams()
  
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False

  def __getNewLine(self, renaming, line):
    'returns a string of chars'
    newline = [renaming[char] for char in line]
    newline = sorted(newline)
    return "".join(newline)

  # TODO: adopted
  # TODO: rename variables
  def __permuteNormalize(self, renaming, constraints):
    'returns a list of strings'
    newbits = len(renaming)
    
    parsedConstraints = parseConfigs(constraints)
    normalizedConstraints = list(normalizeConstraints(parsedConstraints))

    newlines = [self.__getNewLine(renaming, x) for x in normalizedConstraints]

    newlines = list(set(newlines)) # i.e. unique()
    newlines = sorted(newlines)

    return newlines

  def __handleAlphabetPerm(self, perm):
    'returns a tuple of lists'
    renaming = {}
        
    for (x, y) in zip(self.getAlphabeth(), perm):
      renaming[x] = y

    newActive = self.__permuteNormalize(renaming, self.activeConstraints)
    newPassive = self.__permuteNormalize(renaming, self.passiveConstraints)
    newLeaf = self.__permuteNormalize(renaming, self.leafConstraints)
    newRoot = self.__permuteNormalize(renaming, self.rootConstraints)

    return (newActive, newPassive, newLeaf, newRoot)

  def getAlphabeth(self):
    return set(flatten(self.activeConstraints + self.passiveConstraints)) - {' '}

  # TODO: adopted from
  def normalize(self):
    numLabels = len(self.getAlphabeth())
    nums = list(range(numLabels))
    letters = [chr(x + 97) for x in nums] # works only when numLabels < 27
    allPerms = list(itertools.permutations(letters))
    normalized = [self.__handleAlphabetPerm(perm) for perm in allPerms]
    # normalized is a list of tulpes of lists
    normalized = sorted(normalized)[0]
    self.activeConstraints = normalized[0]
    self.passiveConstraints = normalized[1]
    self.leafConstraints = normalized[2]
    self.rootConstraints = normalized[3]
    # return normalized
