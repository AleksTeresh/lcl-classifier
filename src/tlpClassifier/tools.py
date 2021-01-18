import itertools

# Return the list of possible 3-labellings of node with a given degre
def edge_3_labelling(degree):
    return [(a,b,degree-a-b) for a in range(0,degree+1) for b in range(0,degree+1-a)]

# Return the powerset of the given iterable oject
def powerset(that):
    return set(itertools.chain.from_iterable(itertools.combinations(that, r) for r in range(len(that)+1)))

# Transform a configuration from a numerical form to a alpha form
def num_to_alpha_configuration(num_configuration):
    return "A"*num_configuration[0]+"B"*num_configuration[1]+"C"*num_configuration[2]

# Transform a configuration from a alpha form to a numerical form
def alpha_to_num_configuration(alpha_configuration):
    return (alpha_configuration.count('A'),alpha_configuration.count('B'),alpha_configuration.count('C'))

# Transform a set of configurations from a alpha form to a numerical form
def alpha_to_num_constraint( alpha_constraint):
    return [alpha_to_num_configuration(x) for x in alpha_constraint]
