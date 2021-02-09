from typing import NamedTuple, List, Set
from util import onlyOneIsTrue, flatten
from functools import reduce

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
    self.activeAllowAll = activeAllowAll
    
    self.passiveConstraints = passiveConstraints
    if passiveAllowAll:
      self.passiveConstraints = ["".join(alphabet) for _ in passiveConstraints[0].split(' ')]
    self.passiveAllowAll = passiveAllowAll
    
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
