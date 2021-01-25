from typing import NamedTuple, Set

class BinaryRootedTreeProblem:
  allowedConfigs: Set[str]

class TlpProblem:
  white_constraint: Set[str]
  black_constraint: Set[str]
  white_degree: int
  black_degree: int

class GenericProblem:
  def  __init__(
    self,
    activeConstraints: Set[str],
    passiveConstraints: Set[str],
    leafConstraints: Set[str] = {},
    rootConstraints: Set[str] = {},
    activeAllowAll: bool = False,
    passiveAllowAll: bool = False,
    leafAllowAll: bool = True,
    rootAllowAll: bool = True,
    isTree: bool = True,
    isCycle: bool = False,
    isPath: bool = False,
    isDirected: bool = False,
    isRooted: bool = False,
    isBipartite: bool = True,
    isRegular: bool = True,
  ):
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

    self.isBipartite = isBipartite
    self.isRegular = isRegular
  