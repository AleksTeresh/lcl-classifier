CONST = "(1)"
ITERATED_LOG = "(log* n)"
LOGLOG = "(loglog n)"
LOG = "(log n)"
GLOBAL = "(n)"
UNSOLVABLE = "unsolvable"
UNKNOWN = ""

complexities = [CONST, ITERATED_LOG, LOGLOG, LOG, GLOBAL, UNSOLVABLE]

complexityToInt = {
  CONST: 100,
  ITERATED_LOG: 200,
  LOGLOG: 300,
  LOG: 400,
  GLOBAL: 500,
  UNSOLVABLE: 600,
  UNKNOWN: 700
}

intToComplexity = {
  100: CONST,
  200: ITERATED_LOG,
  300: LOGLOG,
  400: LOG,
  500: GLOBAL,
  600: UNSOLVABLE,
  700: UNKNOWN
}
