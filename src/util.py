from functools import reduce

flatMap = lambda f, arr: list(reduce(lambda a, b: a + b, map(f, arr)))

flatten = lambda arr: flatMap(lambda x: x, arr)

def onlyOneIsTrue(a, b, c):
  return (a and not b and not c) or (not a and b and not c) or (not a and not b and c)

def areAllTheSame(list):
  return len(list) == 0 or list.count(list[0]) == len(list)
