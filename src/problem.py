from typing import NamedTuple, List, Set
from util import onlyOneIsTrue
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
    # if activeAllowAll and passiveAllowAll:
    #   throw Exception('problem')

    self.activeConstraints = activeConstraints
    self.activeAllowAll = activeAllowAll
    
    self.passiveConstraints = passiveConstraints
    self.passiveAllowAll = passiveAllowAll
    
    self.leafConstraints = leafConstraints
    self.leafAllowAll = leafAllowAll
    
    self.rootConstraints = rootConstraints
    self.rootAllowAll = rootAllowAll
    
    self.isCycle = isCycle
    self.isPath = isPath
    self.isDirected = isDirected

    self.isTree = isTree
    self.isRooted = isRooted

    self.isRegular = isRegular

    self.__checkParams()
  