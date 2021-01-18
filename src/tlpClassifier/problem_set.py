from enum import Enum

class Problem_set(Enum):
    Unclassified = 0
    Classified = 1

problem_set_name = {
    Problem_set.Unclassified : "UC",
    Problem_set.Classified : "C",
}