import os
import flask
from flask import request, jsonify
from flask_cors import CORS
from webargs import fields, validate
from webargs.flaskparser import use_args
from problem import GenericProblem, ProblemFlags, ProblemProps
from query import Query, QueryExcludeInclude, Bounds
from classifier import classify
from db import getProblem, getProblems
from complexity import *

app = flask.Flask(__name__)
app.config["DEBUG"] = ('FLASK_ENV' not in os.environ or os.environ['FLASK_ENV'] != 'production')
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

@app.route('/api/classifier/problem', methods=['GET'])
@use_args(problem_args, location='query')
def problem(args):
  p = GenericProblem(
    args["active_constraints"],
    args["passive_constraints"],
    args["leaf_constraints"],
    args["root_constraints"],
    leafAllowAll=(args["leaf_constraints"] == []),
    rootAllowAll=(args["root_constraints"] == []),
    flags=ProblemFlags(
      isTree=args["is_tree"],
      isCycle=args["is_cycle"],
      isPath=args["is_path"]
    )
  )

  res = getProblem(p)
  if res is not None:
    return jsonify(res)
  else:
    res = classify(p)
    return jsonify(res.dict())

query_args = {
  "is_tree": fields.Bool(required=True),
  "is_cycle": fields.Bool(required=True),
  "is_path": fields.Bool(required=True),
  "is_directed_or_rooted": fields.Bool(missing=False),
  "is_regular": fields.Bool(missing=False),

  "rand_upper_bound": fields.Str(
    missing=UNSOLVABLE,
    validate=lambda x: x in complexities),
  "rand_lower_bound": fields.Str(
    missing=CONST,
    validate=lambda x: x in complexities),
  "det_upper_bound": fields.Str(
    missing=UNSOLVABLE,
    validate=lambda x: x in complexities),
  "det_lower_bound": fields.Str(
    missing=CONST,
    validate=lambda x: x in complexities),

  "exclude_if_config_has_all_of": fields.List(fields.Str(), missing=[]),
  "exclude_if_config_has_some_of": fields.List(fields.Str(), missing=[]),
  "include_if_config_has_all_of": fields.List(fields.Str(), missing=[]),
  "include_if_config_has_some_of": fields.List(fields.Str(), missing=[]),

  "largest_problem_only": fields.Bool(missing=False),
  "smallest_problem_only": fields.Bool(missing=False),

  "active_degree": fields.Int(required=True),
  "passive_degree": fields.Int(required=True),
  "label_count": fields.Int(required=True),
  "actives_all_same": fields.Bool(missing=False),
  "passives_all_same": fields.Bool(missing=False),
}

@app.route('/api/classifier/query', methods=['GET'])
@use_args(query_args, location='query')
def query(args):
  query = Query(
    props = ProblemProps(
      activeDegree=args['active_degree'],
      passiveDegree=args['passive_degree'],
      labelCount=args['label_count'],
      activesAllSame=args['actives_all_same'],
      passivesAllSame=args['passives_all_same'],
      flags=ProblemFlags(
        isTree=args['is_tree'],
        isCycle=args['is_cycle'],
        isPath=args['is_path'],
        isDirectedOrRooted=args['is_directed_or_rooted'],
        isRegular=args['is_regular'],
      )
    ),
    bounds=Bounds(
      randUpperBound=args['rand_upper_bound'],
      randLowerBound=args['rand_lower_bound'],
      detUpperBound=args['det_upper_bound'],
      detLowerBound=args['det_lower_bound'],
    ),
    excludeInclude=QueryExcludeInclude(
      excludeIfConfigHasAllOf=args['exclude_if_config_has_all_of'],
      excludeIfConfigHasSomeOf=args['exclude_if_config_has_some_of'],
      includeIfConfigHasAllOf=args['include_if_config_has_all_of'],
      includeIfConfigHasSomeOf=args['include_if_config_has_some_of'],
      returnLargestProblemOnly=args['largest_problem_only'],
      returnSmallestProblemOnly=args['smallest_problem_only'],
    )
  )

  res = getProblems(query)
  return jsonify(res)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
  app.run(host='0.0.0.0')
