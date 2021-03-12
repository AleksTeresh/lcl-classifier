import sys, getopt, pickle
from problem import GenericProblem, ProblemFlags, ProblemProps
from classifier import classify
from batch_classify import batchClassify
from generator import generate
from complexity import *
from statistics import compute as computeStats, prettyPrint
from query import Query, Bounds, QueryExcludeInclude
from batch_classify import classifyAndStore, reclassifyAndStore
from db import storeProblemsAndGetWithIds, getClassifiedProblemObjs, getProblem


def generateProblemClass(
    activeDegree,
    passiveDegree,
    labelCount,
    isDirectedOrRooted,
    activesAllSame=False,
    passivesAllSame=False,
    isTree=False,
    isCycle=False,
    isPath=False,
    countLimit=None,
    skipCount=None,
):
    print("Generating the following:")
    print("  activeDegree = %s," % activeDegree)
    print("  passiveDegree = %s," % passiveDegree)
    print("  labelCount = %s," % labelCount)
    print("  isDirectedOrRooted = %s" % isDirectedOrRooted)

    flags = ProblemFlags(
        isTree=isTree,
        isCycle=isCycle,
        isPath=isPath,
        isDirectedOrRooted=isDirectedOrRooted,
    )

    props = ProblemProps(
        activeDegree,
        passiveDegree,
        labelCount,
        activesAllSame,
        passivesAllSame,
        flags=flags,
    )

    query = Query(props)

    ps = generate(
        activeDegree,
        passiveDegree,
        labelCount,
        activesAllSame,
        passivesAllSame,
        flags,
        countLimit=(sys.maxsize if countLimit is None else countLimit),
        skipCount=(0 if skipCount is None else skipCount),
    )

    psWithIds = storeProblemsAndGetWithIds(ps, props)
    classifyAndStore(
        psWithIds,
        props=props,
        countLimit=countLimit if countLimit is None else len(ps),
        skipCount=skipCount,
    )

    res = getClassifiedProblemObjs(query)
    stats = computeStats(res)
    prettyPrint(stats)


generateProblemClass(
    activeDegree=2, passiveDegree=2, labelCount=2, isDirectedOrRooted=False, isPath=True
)

generateProblemClass(
    activeDegree=2,
    passiveDegree=2,
    labelCount=2,
    isDirectedOrRooted=False,
    isCycle=True,
)

generateProblemClass(
    activeDegree=2, passiveDegree=2, labelCount=2, isDirectedOrRooted=True, isPath=True
)

generateProblemClass(
    activeDegree=2, passiveDegree=2, labelCount=2, isDirectedOrRooted=True, isCycle=True
)

generateProblemClass(
    activeDegree=2, passiveDegree=2, labelCount=3, isDirectedOrRooted=False, isPath=True
)

generateProblemClass(
    activeDegree=2, passiveDegree=2, labelCount=3, isDirectedOrRooted=True, isPath=True
)

generateProblemClass(
    activeDegree=2, passiveDegree=2, labelCount=4, isDirectedOrRooted=False, isPath=True
)

generateProblemClass(
    activeDegree=2,
    passiveDegree=2,
    labelCount=4,
    isDirectedOrRooted=True,
    isPath=True,
    countLimit=sys.maxsize,
    skipCount=0,
)

generateProblemClass(
    activeDegree=3, passiveDegree=2, labelCount=2, isDirectedOrRooted=False, isTree=True
)

generateProblemClass(
    activeDegree=3, passiveDegree=2, labelCount=2, isDirectedOrRooted=True, isTree=True
)

generateProblemClass(
    activeDegree=3, passiveDegree=2, labelCount=3, isDirectedOrRooted=False, isTree=True
)

generateProblemClass(
    activeDegree=3,
    passiveDegree=2,
    labelCount=3,
    isDirectedOrRooted=True,
    isTree=True,
    countLimit=sys.maxsize,
    skipCount=0,
)

generateProblemClass(
    activeDegree=3,
    passiveDegree=2,
    labelCount=4,
    isDirectedOrRooted=True,
    isTree=True,
    passivesAllSame=True,
    countLimit=sys.maxsize,
    skipCount=0,
)

generateProblemClass(
    activeDegree=3,
    passiveDegree=2,
    labelCount=3,
    isDirectedOrRooted=True,
    isTree=True,
    passivesAllSame=True,
)

generateProblemClass(
    activeDegree=3,
    passiveDegree=2,
    labelCount=4,
    isDirectedOrRooted=True,
    isTree=True,
    activesAllSame=True,
)
