from problem import GenericProblem
from problem import unparse_configs
from response import GenericResponse
from .classify_context import ClassifyContext
from complexity import CONST, UNSOLVABLE, LOG, LOGLOG
from multiprocessing import Queue
import multiprocessing as mp
import rust2py


def validate(problem: GenericProblem) -> None:
    if problem.flags.is_cycle:
        raise Exception("re", "Cannot classify if the graph is a cycle")

    if problem.flags.is_directed_or_rooted:
        raise Exception("re", "Cannot classify if the tree is rooted")

    if not problem.flags.is_regular:
        raise Exception("re", "Cannot classify if the graph is not regular")

    if not problem.root_allow_all or not problem.leaf_allow_all:
        raise Exception("re", "Leaves and roots must allow all configurations")


def run_r_e(data: str, q: Queue) -> None:
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


def classify(problem: GenericProblem, context: ClassifyContext) -> GenericResponse:
    validate(problem)

    data = (
        "\n".join(
            unparse_configs(
                problem.active_constraints, problem.flags.is_directed_or_rooted
            )
        )
        + "\n\n"
        + "\n".join(
            unparse_configs(
                problem.passive_constraints, problem.flags.is_directed_or_rooted
            )
        )
    )

    timeout_seconds = 0.1 if context.is_batch else 0.5
    # potentially add here things like labels and iter
    # that depend on whether we're operating in a batch mode

    ctx = mp.get_context("fork")
    q = ctx.Queue()
    process = ctx.Process(target=run_r_e, kwargs={"data": data, "q": q})
    process.start()
    try:
        (lower_bound_raw, upper_bound_raw) = q.get(timeout=timeout_seconds)
    except:
        pass
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join()

    if lower_bound_raw == "log n":
        lower_bound = LOG
        lower_bound_rand = LOGLOG
    elif lower_bound_raw == "unknown":
        lower_bound = CONST
        lower_bound_rand = CONST
    else:
        lower_bound = CONST
        lower_bound_rand = CONST

    if upper_bound_raw == "unknown":
        upper_bound = UNSOLVABLE
        upper_bound_rand = UNSOLVABLE
    else:
        upper_bound = CONST
        upper_bound_rand = CONST

    return GenericResponse(
        problem,
        upper_bound_rand,
        lower_bound_rand,
        upper_bound,
        lower_bound,
    )
