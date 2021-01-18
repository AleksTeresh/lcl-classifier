import numpy as np
import itertools, tempfile, re, subprocess,os
import problem
from time import time

LABELS = set([0,1,2])
WHITE_DEGREE = 2
BLACK_DEGREE = 3
SERVER_DIR = os.path.dirname(os.path.realpath(__file__))+'/server'

# Return all the configurations of the given constraint that does not contains any of the given labels
def configurations_without(constraint, that):
    return {elem for elem in constraint if all([elem[i] == 0 for i in that])}

# Remove all the useless configurations from both white and black constraints
def constraint_reduction(white_constraint, black_constraint):
    # Return the alphabet of the given constraint (a set of 3-tuple)
    def constraint_alphabet(constraint):
        alphabet = set()
        for elem in constraint:
            for label in LABELS:
                if elem[label] != 0:
                    alphabet.add(label)
        return alphabet

    # Return the sets of labels that appear in and only in one constraint
    def labels_in_1_constraint(white_constraint,black_constraint):
        return (constraint_alphabet(white_constraint).union(constraint_alphabet(black_constraint))).difference(constraint_alphabet(white_constraint).intersection(constraint_alphabet(black_constraint)))

    tmp = set(LABELS)
    while(len(tmp) != 0 and len(white_constraint)!=0 and len(black_constraint)!=0):
        tmp = labels_in_1_constraint(white_constraint,black_constraint)
        white_constraint = configurations_without(white_constraint,tmp)
        black_constraint = configurations_without(black_constraint,tmp)
    return(white_constraint,black_constraint)


#for tuple (x,x) if alphabet =3
#on the doc (x,x) (ex : 3,2)
def redundancy_algorithm(white_constraint,black_constraint):
    def relabeled_configurations(constraint,i,j):
        tmp = set()
        for elem in constraint:
            if elem[j] != 0 :
                lst = list(elem).copy()
                lst[i] = elem[i]+elem[j]
                lst[j] = 0
                tmp.add(tuple(lst))
        return tmp
        
    for i in LABELS:
        used_labels = LABELS.copy()
        used_labels.remove(i)
        for j in used_labels:
            if relabeled_configurations(white_constraint,i,j).issubset(white_constraint) and\
                relabeled_configurations(black_constraint,i,j).issubset(black_constraint):
                return (configurations_without(white_constraint,set([j])),configurations_without(black_constraint,set([j])), LABELS - set([j]))
    return None


# For tuple (2,3)
# on the doc (3,2)
# could be (3,x)
def greedy4Coloring(problem):
    white = set([(1,1,0),(0,1,1),(1,0,1)])
    black = set([(BLACK_DEGREE,0,0),(0,BLACK_DEGREE,0),(0,0,BLACK_DEGREE)])
    if white == problem.white_constraint and black.issubset(problem.black_constraint) and len(problem.black_constraint) > 3:
        return True

def round_eliminator(problem, function, iterations, labels, search_string):
    with tempfile.NamedTemporaryFile(mode = 'w+',suffix='.txt',newline='\n') as temp_file_w, tempfile.NamedTemporaryFile(mode = 'w+',suffix='.txt',newline='\n') as temp_file_b:
        
        temp_file_b.write(problem.re_format_black())
        temp_file_w.write(problem.re_format_white())

        temp_file_b.flush()
        temp_file_w.flush()

        result_b = subprocess.getoutput(SERVER_DIR + " " + function + ' -f ' + temp_file_b.name + ' --iter ' + str(iterations) +' --labels ' + str(labels))
        result_w = subprocess.getoutput(SERVER_DIR + " " + function + ' -f ' + temp_file_w.name + ' --iter ' + str(iterations) +' --labels ' + str(labels))
        return (result_b, result_w)

def round_eliminator_ub(problem, iterations, labels):
    result_b, result_w = round_eliminator(problem, 'autoub', iterations, labels, 'Upper bound of ')
    if not result_b and not result_w:
        return -1
        
    def get_value(result):
        for i in range(1000):
            search_string_i  = 'Upper bound of ' + str(i)
            if result.find(search_string_i) != -1:
                return i
        return -1
        
    w = get_value(result_w) if result_w else -1
    b = get_value(result_b) if result_b else -1
    if w == -1:
        return b
    if b == -1:
        return w
    return min(w,b)

def round_eliminator_lb(problem, iterations, labels):
    result_b, result_w = round_eliminator(problem, 'autolb', iterations, labels, 'Lower bound of ')
    if not result_b and not result_w:
        return -1
        
    def get_value(result):
        for i in reversed(range(1000)):
            search_string_i  = 'Lower bound of ' + str(i)
            if result.find(search_string_i) != -1:
                return i
        return -1
    w = get_value(result_w) if result_w else -1
    b = get_value(result_b) if result_b else -1
    if w > problem.constant_upper_bound:
        return b
    if b > problem.constant_upper_bound:
        return w
    return max(w,b)

def cover_map_1(white_constraint,black_constraint):
    w = set([(w0-b0,w1-b1,w2-b2) for (w0,w1,w2) in black_constraint for (b0,b1,b2) in white_constraint if w0-b0 >= 0 and w1-b1 >=0 and w2-b2>=0])
    b = set([(w0a+w0b,w1a+w1b,w2a+w2b) for (w0a,w1a,w2a) in w for (w0b,w1b,w2b) in w if (w0a+w0b,w1a+w1b,w2a+w2b) in white_constraint])
    return not b