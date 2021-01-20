from typing import NamedTuple, Set

class BinaryRootedTreeProblem(NamedTuple):
  allowedConfigs: Set[str]

class TlpProblem(NamedTuple):
  white_constraint: Set[str]
  black_constraint: Set[str]
  white_degree: int
  black_degree: int

class GenericProblem(NamedTuple):
  activeConstraints: Set[str]
  activeAllowAll: bool
  
  passiveConstraints: Set[str]
  passiveAllowAll: bool
  
  leafConstraints: Set[str]
  leafAllowAll: bool
  
  rootConstraints: Set[str]
  rootAllowAll: bool
  
  isCycle: bool
  isPath: bool
  isDirected: bool

  isTree: bool
  isRooted: bool

  isBipartite: bool
  isRegular: bool
  