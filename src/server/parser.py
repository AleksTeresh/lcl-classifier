from util import flatMap, flatten

def splitConfig(config):
  res = flatten([x.split(' ') for x in config.split(' : ')])
  return [x for x in res if x.strip() != '']

def validLabelsFromEdge(edgeConfig):
  halfBracketSplit = edgeConfig.split('(')
  halfBracketSplit = [halfBracketSplit[0]] + ['(' + x for x in halfBracketSplit[1:]]
  halfBracketSplit = [x for x in halfBracketSplit if len(x) > 0]
  
  fullBracketSplit = flatMap(lambda x: [y for y in x.split(')') if len(y) > 0], halfBracketSplit)
  fullBracketSplit = [(x + ')') if x[0] == '(' else x for x in fullBracketSplit]

  return flatMap(lambda x: [x] if x[0] == '(' else list(x), fullBracketSplit)

def parseConfig(config):
  config = config.strip()
  perEdge = splitConfig(config)
  degree = len(perEdge)
  labelsPerEdge = [validLabelsFromEdge(x) for x in perEdge]

  return labelsPerEdge
  
def parseConfigs(configs):
  configs = [x for x in configs if x.strip() != '']
  return [parseConfig(config) for config in configs]

def unparseConfig(config, isDirectedOrRooted):
  if isDirectedOrRooted and len(config) > 1:
    config = config[0] + ':' + config[1:]
  return " ".join(config)

def unparseConfigs(configs, isDirectedOrRooted):
  return [unparseConfig(config, isDirectedOrRooted) for config in configs]
