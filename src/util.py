from functools import reduce

flatMap = lambda f, arr: list(reduce(lambda a, b: a + b, map(f, arr)))

def onlyOneIsTrue(a, b, c):
  return (a and not b and not c) or (not a and b and not c) or (not a and not b and c)
