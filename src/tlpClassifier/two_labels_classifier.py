from bitarray import bitarray,util
from complexity import Complexity

def is_unsolvable(white_constraint,black_constraint,white_degree,black_degree):
    #I.a, I.c
    if (white_constraint[0] == 1 and not white_constraint[1:].any() and black_constraint[0] == 0):
        return True
    #I.b, I.d
    expected_white_constraint = util.zeros(white_degree+1)
    expected_white_constraint[white_degree] = 1
    if (white_constraint == expected_white_constraint and black_constraint[black_degree] == 0):
        return True
    #II.a, II.b
    if (not white_constraint.any()):
        return True
    return False

def is_constant(white_constraint,black_constraint,white_degree,black_degree):
    #III.a, III.b
    if(white_constraint.all() and black_constraint.any() or\
        black_constraint.all() and white_constraint.any()):
        return True
    #IV.a
    if(white_constraint[0] == 1 and black_constraint[0] == 1):
        return True
    #IV.b
    if(white_constraint[white_degree] == 1 and black_constraint[black_degree] == 1):
        return True
    return False

def is_global(white_constraint,black_constraint,white_degree,black_degree):
    #V.a, V.b
    if(white_constraint[0] == 1 and white_constraint[white_degree] == 1 and white_constraint[1:white_degree] == util.zeros(white_degree-1) and\
        black_degree == 2 and black_constraint == bitarray('010')):
        return True
    #VI.a VI.b
    if(white_constraint[:white_degree-1] == util.zeros(white_degree-1) and white_constraint[white_degree-1] == 1 and black_constraint[1] == 1 and black_constraint[2:] == util.zeros(black_degree-1)):
        return True
    return False
    
# Given 2 bitarrays of length at least 2, return the complexity of the corresponding binary labelling problem
def get_complexity_of(white_constraint,black_constraint):
    white_d = len(white_constraint)-1
    black_d = len(black_constraint)-1
    assert(white_d>=2 and black_d>=2)
    if(is_unsolvable(white_constraint,black_constraint,white_d,black_d) or is_unsolvable(black_constraint,white_constraint,black_d,white_d)):
        return Complexity.Unsolvable
    if(is_constant(white_constraint,black_constraint,white_d,black_d)):
        return Complexity.Constant
    if(is_global(white_constraint,black_constraint,white_d,black_d) or is_global(black_constraint,white_constraint,black_d,white_d)):
        return Complexity.Global
    return Complexity.Logarithmic

# Transform a problem that uses only two labels in 2 bitarrays.
def constraints_to_bitvector_tuple(white_constraint,black_constraint,alphabet,white_degree,black_degree):
    if not len(alphabet) < 3:
        print("Error, the constraints have more than 2 labels")
        return
    white = util.zeros(white_degree+1)
    black = util.zeros(black_degree+1)
    label = list(alphabet)[0]
    for configuration in white_constraint:
        white[configuration[label]] = 1
    for configuration in black_constraint:
        black[configuration[label]] = 1
    return (white,black)