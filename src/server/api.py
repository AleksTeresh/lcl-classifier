import os
import flask
from typing import List, Dict
from flask import jsonify
from flask_cors import CORS
from webargs import fields
from webargs.flaskparser import use_args
from problem import GenericProblem, ProblemFlags, ProblemProps
from query import Query, QueryExcludeInclude, Bounds
from classify import classify
from statistics import compute as compute_stats
from db import get_classified_problem_obj
from db import get_classified_problem_objs
from db import get_batch_classifications
from db import get_problem_count
from db import store_problem_and_classification
from db import get_batch_classification_by_query
from complexity import CONST, UNSOLVABLE, complexities


def is_query_response_complete(batches: List[Dict]) -> bool:
    return (
        len(batches) != 0
        and batches[-1]["count_limit"] is None
        and batches[-1]["skip_count"] == 0
    )


app = flask.Flask(__name__)
app.config["DEBUG"] = (
    "FLASK_ENV" not in os.environ or os.environ["FLASK_ENV"] != "production"
)
CORS(app)

problem_args = {
    "is_tree": fields.Bool(required=True),
    "is_cycle": fields.Bool(required=True),
    "is_path": fields.Bool(required=True),
    "active_constraints": fields.List(fields.Str(), missing=[]),
    "passive_constraints": fields.List(fields.Str(), missing=[]),
    "leaf_constraints": fields.List(fields.Str(), missing=[]),
    "root_constraints": fields.List(fields.Str(), missing=[]),
}


@app.route("/api/classifier/problem", methods=["GET"])
@use_args(problem_args, location="query")
def problem(args):
    p = GenericProblem(
        args["active_constraints"],
        args["passive_constraints"],
        args["leaf_constraints"],
        args["root_constraints"],
        leaf_allow_all=(args["leaf_constraints"] == []),
        root_allow_all=(args["root_constraints"] == []),
        flags=ProblemFlags(
            is_tree=args["is_tree"], is_cycle=args["is_cycle"], is_path=args["is_path"]
        ),
    )

    # classified_problem = get_classified_problem_obj(p)
    # if classified_problem is not None:
    #     return jsonify(
    #         {
    #             "problem": classified_problem.to_problem().dict(),
    #             "result": classified_problem.to_response().dict(),
    #         }
    #     )
    # else:
    res = classify(p)
        # if not (
        #     res.det_lower_bound == CONST
        #     and res.det_upper_bound == UNSOLVABLE
        #     and res.rand_lower_bound == CONST
        #     and res.rand_upper_bound == UNSOLVABLE
        # ):
        #     store_problem_and_classification(p, res)
    return jsonify({"problem": p.dict(), "result": res.dict()})


query_args = {
    "is_tree": fields.Bool(required=True),
    "is_cycle": fields.Bool(required=True),
    "is_path": fields.Bool(required=True),
    "is_directed_or_rooted": fields.Bool(missing=False),
    # is_regular is not currently selectable in fornt-end
    # since currently the tool works only with regular trees anyway.
    # This might change in the future though
    "is_regular": fields.Bool(missing=True),
    "rand_upper_bound": fields.Str(
        missing=UNSOLVABLE, validate=lambda x: x in complexities
    ),
    "rand_lower_bound": fields.Str(missing=CONST, validate=lambda x: x in complexities),
    "det_upper_bound": fields.Str(
        missing=UNSOLVABLE, validate=lambda x: x in complexities
    ),
    "det_lower_bound": fields.Str(missing=CONST, validate=lambda x: x in complexities),
    "exclude_if_config_has_all_of": fields.List(fields.Str(), missing=[]),
    "exclude_if_config_has_some_of": fields.List(fields.Str(), missing=[]),
    "include_if_config_has_all_of": fields.List(fields.Str(), missing=[]),
    "include_if_config_has_some_of": fields.List(fields.Str(), missing=[]),
    "largest_problem_only": fields.Bool(missing=False),
    "smallest_problem_only": fields.Bool(missing=False),
    "completely_rand_unclassified_only": fields.Bool(missing=False),
    "partially_rand_unclassified_only": fields.Bool(missing=False),
    "completely_det_unclassified_only": fields.Bool(missing=False),
    "partially_det_unclassified_only": fields.Bool(missing=False),
    "active_degree": fields.Int(required=True),
    "passive_degree": fields.Int(required=True),
    "label_count": fields.Int(required=True),
    "actives_all_same": fields.Bool(missing=False),
    "passives_all_same": fields.Bool(missing=False),
    "fetch_stats_only": fields.Bool(missing=True),
}


@app.route("/api/classifier/query", methods=["GET"])
@use_args(query_args, location="query")
def query(args):
    query = Query(
        props=ProblemProps(
            active_degree=args["active_degree"],
            passive_degree=args["passive_degree"],
            label_count=args["label_count"],
            actives_all_same=args["actives_all_same"],
            passives_all_same=args["passives_all_same"],
            flags=ProblemFlags(
                is_tree=args["is_tree"],
                is_cycle=args["is_cycle"],
                is_path=args["is_path"],
                is_directed_or_rooted=args["is_directed_or_rooted"],
                is_regular=args["is_regular"],
            ),
        ),
        bounds=Bounds(
            rand_upper_bound=args["rand_upper_bound"],
            rand_lower_bound=args["rand_lower_bound"],
            det_upper_bound=args["det_upper_bound"],
            det_lower_bound=args["det_lower_bound"],
        ),
        exclude_include=QueryExcludeInclude(
            exclude_if_config_has_all_of=args["exclude_if_config_has_all_of"],
            exclude_if_config_has_some_of=args["exclude_if_config_has_some_of"],
            include_if_config_has_all_of=args["include_if_config_has_all_of"],
            include_if_config_has_some_of=args["include_if_config_has_some_of"],
            return_largest_problem_only=args["largest_problem_only"],
            return_smallest_problem_only=args["smallest_problem_only"],
            completely_rand_unclassifed_only=args["completely_rand_unclassified_only"],
            partially_rand_unclassified_only=args["partially_rand_unclassified_only"],
            completely_det_unclassifed_only=args["completely_det_unclassified_only"],
            partially_det_unclassified_only=args["partially_det_unclassified_only"],
        ),
    )

    problems = get_classified_problem_objs(query)
    stats = compute_stats(problems)
    batches = get_batch_classification_by_query(query)
    is_response_complete = is_query_response_complete(batches)
    response = {
        "problems": (
            None
            if args["fetch_stats_only"]
            else [
                {**p.to_unparsed_problem().dict(), **p.to_response().dict()}
                for p in problems
            ]
        ),
        "stats": stats.dict(),
        "is_complete": is_response_complete,
    }
    return jsonify(response)


@app.route("/api/batch_classifications", methods=["GET"])
def batch_classifications():
    classifications = get_batch_classifications()
    return jsonify(classifications)


@app.route("/api/problem_count", methods=["GET"])
def problem_count():
    problem_count = get_problem_count()
    return jsonify({"problem_count": problem_count})


@app.errorhandler(Exception)
def handle_exception(e: Exception):
    print(e)
    args = e.args
    if len(args) < 2:
        return jsonify({"error": "Something went wrong"}), 500

    if args[0] == "problem":
        return jsonify({"error": args[1]}), 400

    if args[0] == "classification-contradiction":
        return jsonify({"error": args[1]}), 500


@app.errorhandler(404)
def page_not_found(e: Exception):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0")
