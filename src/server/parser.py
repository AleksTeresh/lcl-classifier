from util import flatMap, flatten

def splitConfig(config):
  return flatten([x.split(' ') for x in config.split(' : ')])

def validLabelsFromEdge(edgeConfig):
  halfBracketSplit = edgeConfig.split('(')
  halfBracketSplit = [halfBracketSplit[0]] + ['(' + x for x in halfBracketSplit[1:]]
  halfBracketSplit = [x for x in halfBracketSplit if len(x) > 0]
  
  fullBracketSplit = flatMap(lambda x: [y for y in x.split(')') if len(y) > 0], halfBracketSplit)
  fullBracketSplit = [(x + ')') if x[0] == '(' else x for x in fullBracketSplit]

  return flatMap(lambda x: [x] if x[0] == '(' else list(x), fullBracketSplit)

def parseConfig(config):
  perEdge = splitConfig(config)
  degree = len(perEdge)
  labelsPerEdge = [validLabelsFromEdge(x) for x in perEdge]

  return labelsPerEdge
  
def parseConfigs(configs):
  return [parseConfig(config) for config in configs]
