#!/usr/bin/env python3

if __name__ == "__main__":
    from common import get_constraints_for_labels
else:
    from .common import get_constraints_for_labels

from math import gcd
from functools import reduce

def listGcd(arr):
  return reduce(gcd, arr)

def countWalks(graph, src, dst, maxWalkLength):
    # Table to be filled up using DP.
    # The value count[i][j][e] will
    # store count of possible walks from
    # i to j with exactly k edges
    count = {i: {j: [0 for k in range(maxWalkLength + 1)] for j in graph} for i in graph}

    # Loop for number of edges from 0 to k
    for e in range(maxWalkLength + 1):
        for i in graph:  # for source
            for j in graph:  # for destination
                # initialize value
                count[i][j][e] = 0

                # from base cases
                if e == 0 and i == j:
                    count[i][j][e] = 1
                if e == 1 and (j in graph[i]):
                    count[i][j][e] = 1

                # go to adjacent only when the
                # number of edges is more than 1
                if e > 1:
                    for a in graph:
                        if a in graph[i]:  # adjacent of source i
                            count[i][j][e] += count[a][j][e - 1]
    return count[src][dst]

def isFlexible(graph, node):
    walkCounts = countWalks(graph, node, node, 2 * len(graph))
    bigL = []
    for idx, count in enumerate(walkCounts):
        if idx > 0 and count > 0:  # disregard a walk with 0 edges
            bigL.append(idx)
    return len(bigL) > 0 and listGcd(bigL) == 1


def inflexible_labels(constraints, labels):
    constraints_for_labels = get_constraints_for_labels(constraints,labels)
    graph = {label: [] for label in labels}
    for label in labels:
        for constraint in constraints_for_labels[label]:
            if constraint[0] not in graph[label]:
                graph[label].append(constraint[0])
            if constraint[1] not in graph[label]:
                graph[label].append(constraint[1])
    il = []
    for label in labels:
        if not isFlexible(graph, label):
            il.append(label)
    return il

def is_log_solvable(constraints):
    labels = list(set("".join(constraints)))

    while il := inflexible_labels(constraints, labels):
        updated_constraints = []
        for constraint in constraints:
            if not (set(il) & set(constraint)): # keep only flexible labels
                updated_constraints.append(constraint)
        constraints = updated_constraints
        labels = list(set("".join(constraints)))
    
    return True if constraints else False

def log_decider(constraints):
    if is_log_solvable(constraints):  # is not empty
        print("O(log n)")
    else:
        print("Ω(n)")

if __name__ == "__main__":
    constraints = input().split()
    log_decider(constraints)
