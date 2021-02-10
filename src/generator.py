from problem import GenericProblem

tlpProblem1 = GenericProblem(
  ['A B', 'C C', 'D A'],
  ['B B C', 'A A A', 'B B B', 'A A C', 'B C C', 'Y X B']
)
tlpProblem1.normalize()

tlpProblem2 = GenericProblem(
  ['A C', 'B B'],
  ['C C B', 'A A A', 'C C C', 'A A B', 'C B B']
)
tlpProblem2.normalize()

print(tlpProblem1.activeConstraints)
print(tlpProblem1.passiveConstraints)
print(tlpProblem2.activeConstraints)
print(tlpProblem2.passiveConstraints)
