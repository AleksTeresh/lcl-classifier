from complexity import Complexity, complexity_name
from enum import Enum
import itertools
from algorithms import constraint_reduction
from tools import alpha_to_num_constraint,num_to_alpha_configuration
LABELS = [0,1,2]
import sys
class Constraints(Enum):
    White = 0
    Black = 1 

class Problem:

    # Create a Problem
    def __init__(self, white_constraint, black_constraint, white_degree, black_degree):
        self.white_constraint,self.black_constraint = map(lambda x : frozenset(x),constraint_reduction(frozenset(white_constraint),frozenset(black_constraint)))
        self.white_degree = white_degree
        self.black_degree = black_degree
        self.lower_bound = Complexity.Constant
        self.upper_bound = Complexity.Unsolvable
        self.constant_upper_bound = sys.maxsize
        self.constant_lower_bound = 0
    # The hash function for problems
    def __hash__(self):
        return hash((self.white_constraint,self.black_constraint))

    # Equality of problem.
    def __eq__(self,other):
        return (self.white_constraint == other.white_constraint and self.black_constraint == other.black_constraint)

    # Print the main characteristics of the problem in the console
    def __repr__(self):
        w = ", ".join(map(num_to_alpha_configuration,self.white_constraint))
        b = ", ".join(map(num_to_alpha_configuration,self.black_constraint))
        res = w + "\n" + b + "\n"
        if(self.get_complexity() == Complexity.Unclassified):
            return  res + "Lower bound : "+ complexity_name[self.lower_bound] + "\n" + "Upper bound : " + complexity_name[self.upper_bound] + "\n"
        else :
            res = res + "Complexity : "+ complexity_name[self.lower_bound] + "\n"
        if(self.get_complexity() == Complexity.Constant):
            res += str(self.constant_lower_bound) + " round(s) lower bound\n"
            return res + str(self.constant_upper_bound) + " round(s) upper bound\n"
        return res

    def to_tuple(self):
        w = ", ".join(map(num_to_alpha_configuration,self.white_constraint))
        b = ", ".join(map(num_to_alpha_configuration,self.black_constraint))
        if self.get_complexity() == Complexity.Unclassified:
            return {"white constraint" : w, "black constraint" : b, "complexity lower bound" : complexity_name[self.lower_bound], "complexity upper bound" : complexity_name[self.upper_bound]}
        if self.get_complexity() == Complexity.Constant:
            return {"white constraint" : w, "black constraint" : b, "complexity" : complexity_name[self.get_complexity()], "complexity lower bound" : self.constant_lower_bound, "complexity upper bound" : self.constant_upper_bound}
        else:
            return {"white constraint" : w, "black constraint" : b, "complexity" : complexity_name[self.get_complexity()]}


    # Write the main characteristics of the problem in a file
    def write_in_file(self, io):
        io.write(self.__repr__()+"\n")

    def re_format(self):
        def mapping_function(configuration):
            return "A "*configuration[0]+"B "*configuration[1]+"C "*configuration[2]+"\n"

        w = "".join(map(mapping_function,self.white_constraint))
        b = "".join(map(mapping_function,self.black_constraint))
        return(w,b)

    def re_format_white(self):
        w,b = self.re_format()
        return(w + '\n'+b)

    def re_format_black(self):
        w,b = self.re_format()
        return(b + '\n'+w)

    # Return the alphabet of the given constraint
    def constraint_alphabet(self, constraint):
        alphabet = set()
        config = self.black_constraint if constraint == Constraints.Black else self.white_constraint
        for elem in config:
            for label in LABELS:
                if elem[label] != 0:
                    alphabet.add(label)
        return alphabet 

    # Return the size of the alphabet of the given constraint
    def constraint_size(self, constraint):
        return len(self.black_constraint if constraint == Constraints.Black else self.white_constraint)

    # Return the the alphabet of the problem
    def alphabet(self):
        return self.constraint_alphabet(Constraints.White).union(self.constraint_alphabet(Constraints.Black))

    # Return the the alphabet size of the problem
    def alphabet_size(self):
        return len(self.alphabet())
    

    # Check if the current problem is a restriction of the given problem
    def is_restriction(self, other):
        return self.white_constraint.issubset(other.white_constraint) and self.black_constraint.issubset(other.black_constraint)

     # Check if the current problem is a relaxation of the given problem
    def is_relaxation(self, other):
        return other.is_restriction(self)

    # Set a lower bound for the complexity of the problem
    def set_lower_bound(self,complexity):
        if self.upper_bound.value < complexity.value:
            print("Error, trying to put a lower bound (", complexity, ") bigger than the current upper bound (", self.upper_bound , ")")
            print(self)
            return
        if self.lower_bound.value < complexity.value:
            self.lower_bound = complexity
            if complexity == Complexity.Unsolvable:
                self.set_upper_bound(Complexity.Unsolvable)

    # Set an upper bound for the complexity of the problem
    def set_upper_bound(self,complexity):
        if self.lower_bound.value > complexity.value:
            print("Error, trying to put a upper bound (", complexity, ") lower than the current lower bound (", self.lower_bound , ")")
            print(self)
        if self.upper_bound.value > complexity.value:
            self.upper_bound = complexity
            if complexity == Complexity.Constant:
                self.set_lower_bound(Complexity.Constant)


    # Set the complexity of the problem to the given complexity
    def set_complexity(self,complexity):
        if self.lower_bound == self.upper_bound and self.lower_bound != Complexity.Unclassified and self.lower_bound != complexity:
            print("error a different complexity has already been assigned")
        self.set_lower_bound(complexity)
        self.set_upper_bound(complexity)

    # Get the complexity of the problem
    def get_complexity(self):
        return self.lower_bound if (self.lower_bound == self.upper_bound) else Complexity.Unclassified

    # Return a list of equivalents problem to the given problem as constraints tuple
    def equivalent_problems(self):
        x = (self.white_constraint,self.black_constraint)
        problemList = [[[ (t[a],t[b],t[c]) for t in x] for x in x] for a,b,c in itertools.permutations([0,1,2])]
        if self.black_degree == self.white_degree:
            problemList+=([[b,w] for w,b in problemList])
        return problemList

    # Return a list of equivalents problem to the given problem
    def equivalent_problems_instance(self):
        return [Problem(w,b,self.white_degree,self.black_degree) for w,b in self.equivalent_problems()]
    
    # Return the characteristic problem of the equiavalent class of problems of this problem
    def get_characteristic_problem(self):
        equivalent_problems_list = self.equivalent_problems()
        for white,black in equivalent_problems_list:
            white.sort()
            black.sort() 
        equivalent_problems_list.sort()
        white_c,black_c = equivalent_problems_list[0]
        return Problem(white_c,black_c,self.white_degree,self.black_degree)

    # Return true if and only if the given problem is the unique characteristic problem of all of its equivalents problems
    def is_characteristic_problem(self):
        return self.get_characteristic_problem() == self

# Return an instance of a problem given an problem in an alpha form
def alpha_to_problem(white_constraint,black_constraint):
    if len(white_constraint)==0 or len(black_constraint) == 0:
        return
    white_degree = len(list(white_constraint)[0])
    black_degree = len(list(black_constraint)[0])
    degrees = [(white_degree,white_constraint),(black_degree,black_constraint)]
    degrees.sort(key=lambda tup: tup[0])
    return Problem(alpha_to_num_constraint(degrees[0][1]),alpha_to_num_constraint(degrees[1][1]),degrees[0][0],degrees[1][0]).get_characteristic_problem()