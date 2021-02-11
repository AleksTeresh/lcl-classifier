from problem import GenericProblem

tlpProblem1 = GenericProblem(
  ['A B', 'C C', 'D ADC'],
  ['B B C', 'A A A', 'B B B', 'A A C', 'B C C', 'Y X B']
)
tlpProblem1.normalize()

tlpProblem2 = GenericProblem(
  ['A C', 'B B'],
  ['C C B', 'A A A', 'C C C', 'A A B', 'C B B']
)
tlpProblem2.normalize()

tlpProblem3 = GenericProblem(
  ['a a a', 'b a a', 'c a a'],
  ['a a', 'b b', 'c c'],
)
tlpProblem3.normalize()

tlpProblem4 = GenericProblem(
  ['a a a', 'b a a', 'c a a'],
  ['a a', 'b b', 'c c'],
  isTree=True, isCycle=False, isPath=False,
  isRooted=True
)
tlpProblem4.normalize()

print(tlpProblem3.activeConstraints)
print(tlpProblem3.passiveConstraints)
print(tlpProblem3.leafConstraints)

print(tlpProblem4.activeConstraints)
print(tlpProblem4.passiveConstraints)
print(tlpProblem4.leafConstraints)

