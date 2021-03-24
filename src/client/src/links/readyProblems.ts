export const readyProblems = [
  {
    text: 'Sinkless orientation',
    href: `${window.location.origin}/?problem_activeConstraints=A+AB+AB&problem_passiveConstraints=A+B&problem_graphType=tree`
  },
  {
    text: 'Artificial one-round problem',
    href: `${window.location.origin}/?problem_activeConstraints=M+U+U+U%0APM+PM+PM+PM&problem_passiveConstraints=M+UP+UP+UP%0AU+U+U+U&problem_graphType=tree`
  },
  {
    text: 'One-round solvable problem on rooted binary trees',
    href: `${window.location.origin}/?problem_activeConstraints=A+%3A+A%0AC+%3A+C&problem_passiveConstraints=A+%3A+A+A%0AA+%3A+A+C&problem_graphType=tree`
  },
  {
    text: 'Unsolvable problem on rooted binary trees',
    href: `${window.location.origin}/?problem_activeConstraints=B+%3A+B%0AC+%3A+C&problem_passiveConstraints=B+%3A+B+C&problem_graphType=tree`
  },
  {
    text: '2-coloring on undirected cycle',
    href: `${window.location.origin}/?problem_activeConstraints=A+A%0AB+B&problem_passiveConstraints=A+B&problem_graphType=cycle`
  },
  {
    text: '3-coloring on directed cycle',
    href: `${window.location.origin}/?problem_activeConstraints=A+%3A+A%0AB+%3A+B%0AC+%3A+C&problem_passiveConstraints=A+%3A+BC%0AB+%3A+AC%0AC+%3A+AB%0A&problem_graphType=cycle`
  },
  {
    text: 'Forbidden degree or sinkless orientation (fixed point)',
    href: `${window.location.origin}/?problem_activeConstraints=A+X+X%0AH+H+X%0AT+T+T&problem_passiveConstraints=X+AHTX%0AH+T&problem_graphType=tree`
  },
]
