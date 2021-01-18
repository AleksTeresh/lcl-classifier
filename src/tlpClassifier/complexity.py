from enum import Enum

class Complexity(Enum):
    Constant = 0
    Iterated_Logarithmic = 1
    Logarithmic = 2
    Global = 3
    Unsolvable = 4
    Unclassified = 5

complexity_name = {
    Complexity.Unsolvable : "unsolvable",
    Complexity.Constant : "constant",
    Complexity.Iterated_Logarithmic : "iterated_logarithmic",
    Complexity.Logarithmic : "logarithmic",
    Complexity.Global : "global",
    Complexity.Unclassified : "unclassified"
    }