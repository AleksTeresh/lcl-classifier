from problem import GenericProblem
from problem import unparseConfigs
from response import GenericResponse
from .classify_context import ClassifyContext
from complexity import *
from multiprocessing import Process, Queue
import multiprocessing as mp
import bin.rust2py as rust2py


def validate(problem: GenericProblem):
    if problem.flags.isCycle:
        raise Exception("re", "Cannot classify if the graph is a cycle")

    if problem.flags.isDirectedOrRooted:
        raise Exception("re", "Cannot classify if the tree is rooted")

    if not problem.flags.isRegular:
        raise Exception("re", "Cannot classify if the graph is not regular")

    if not problem.rootAllowAll or not problem.leafAllowAll:
        raise Exception("re", "Leaves and roots must allow all configurations")


def runRE(data, q):
    (lb, ub) = rust2py.get_complexity(
        data,
        # if pp_only is set to True, labels param does not matter
        # since it essentially not being used anywhere
        labels=7,
        iter=5,
        merge=False,
        autolb_features="diag,addarrow",
        autoub_features="pred",
        pp_only=True,
    )
    q.put((lb, ub))


def classify(p: GenericProblem, context: ClassifyContext):
    validate(p)

    data = (
        "\n".join(unparseConfigs(p.activeConstraints, p.flags.isDirectedOrRooted))
        + "\n\n"
        + "\n".join(unparseConfigs(p.passiveConstraints, p.flags.isDirectedOrRooted))
    )

    timeoutSeconds = 0.1 if context.isBatch else 0.5
    # potentially add here things like labels and iter
    # that depend on whether we're operating in a batch mode

    ctx = mp.get_context("fork")
    q = ctx.Queue()
    p = ctx.Process(target=runRE, kwargs={"data": data, "q": q})
    p.start()
    try:
        (lowerBoundRaw, upperBoundRaw) = q.get(timeout=timeoutSeconds)
    except:
        pass
    p.join(timeoutSeconds)
    if p.is_alive():
        p.terminate()
        p.join()

    if lowerBoundRaw == "log n":
        lowerBound = LOG
        lowerBoundRand = LOGLOG
    elif lowerBoundRaw == "unknown":
        lowerBound = CONST
        lowerBoundRand = CONST
    else:
        lowerBound = CONST
        lowerBoundRand = CONST

    if upperBoundRaw == "unknown":
        upperBound = UNSOLVABLE
        upperBoundRand = UNSOLVABLE
    else:
        upperBound = CONST
        upperBoundRand = CONST

    return GenericResponse(
        p,
        upperBoundRand,
        lowerBoundRand,
        upperBound,
        lowerBound,
    )
