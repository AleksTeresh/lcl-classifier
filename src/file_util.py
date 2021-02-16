import os
from problem import ProblemFlags

def getProblemDir():
  return os.path.dirname(os.path.realpath(__file__)) + '/problems/'

def getFilenameSuffix(
  activeDegree,
  passiveDegree,
  labelCount,
  props
):
  return (f'_{activeDegree}_{passiveDegree}_{labelCount}' +
  ('t' if props.activesAllSame else 'f') +
  ('t' if props.passivesAllSame else 'f') +
  ('t' if props.flags.isTree else 'f') +
  ('t' if props.flags.isCycle else 'f') +
  ('t' if props.flags.isPath else 'f') +
  ('t' if props.flags.isDirected else 'f') +
  ('t' if props.flags.isRooted else 'f') +
  ('t' if props.flags.isRegular else 'f') +
  '.json')

def getResultFilepath(
  activeDegree,
  passiveDegree,
  labelCount,
  props
):
  return (
    getProblemDir() +
    'results' +
    getFilenameSuffix(
      activeDegree,
      passiveDegree,
      labelCount,
      props
    )
  )

def getProblemFilepath(
  activeDegree,
  passiveDegree,
  labelCount,
  props
):
  return (
    getProblemDir() +
    'problems' +
    getFilenameSuffix(
      activeDegree,
      passiveDegree,
      labelCount,
      props
    )
  )
