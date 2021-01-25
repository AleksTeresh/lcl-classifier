from util import flatMap

def splitConfig(config):
  return config.split(' ')

def validLabelsFromEdge(edgeConfig):
  halfBracketSplit = edgeConfig.split('(')
  halfBracketSplit = [x for x in halfBracketSplit if len(x) > 0]
  # halfBracketSplit = ['(' + x for x in halfBracketSplit]

  fullBracketSplit = flatMap(lambda x: [y for y in x.split(')') if len(y) > 0], halfBracketSplit)
  # fullBracketSplit = [x + ')' for x in fullBracketSplit]

  return fullBracketSplit

def parseConfig(config):
  perEdge = splitConfig(config)
  degree = len(perEdge)
  labelsPerEdge = [validLabelsFromEdge(x) for x in perEdge]

  return labelsPerEdge
  
def parseConfigs(configs):
  return [parseConfig(config) for config in configs]
