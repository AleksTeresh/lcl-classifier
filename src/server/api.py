import os
import flask
from flask import request, jsonify
from flask_cors import CORS
from webargs import fields, validate
from webargs.flaskparser import use_args
from problem import GenericProblem, ProblemFlags, ProblemProps
from query import Query, QueryExcludeInclude, Bounds
from classifier import classify
from statistics import compute as computeStats
from db import getClassifiedProblemObj, getClassifiedProblemObjs, getBatchClassifications, getProblemCount
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

  res = getClassifiedProblemObj(p)
  if res is not None:
    res = res.toResponse()
    return jsonify(res.dict())
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
      completelyRandUnclassifedOnly=args['completely_rand_unclassified_only'],
      partiallyRandUnclassifiedOnly=args['partially_rand_unclassified_only'],
      completelyDetUnclassifedOnly=args['completely_det_unclassified_only'],
      partiallyDetUnclassifiedOnly=args['partially_det_unclassified_only'],
    )
  )

  problems = getClassifiedProblemObjs(query)
  stats = computeStats(problems)
  response = {
    'problems': (None
      if args['fetch_stats_only']
      else [{
        **p.toUnparsedProblem().dict(),
        **p.toResponse().dict()
      } for p in problems]),
    'stats': stats.dict()
  }
  return jsonify(response)

@app.route('/api/batch_classifications', methods=['GET'])
def batchClassifications():
  classifications = getBatchClassifications()
  return jsonify(classifications)

@app.route('/api/problem_count', methods=['GET'])
def problemCount():
  problemCount = getProblemCount()
  return jsonify({
    "problemCount": problemCount
  })

@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    args = e.args
    if len(args) < 2:
      return jsonify({
        'error': 'Something went wrong'
      }), 500

    if args[0] == 'problem':
      return jsonify({
        'error': args[1]
      }), 400

    if args[0] == 'classification-contradiction':
      return jsonify({
        'error': args[1]
      }), 500

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
  app.run(host='0.0.0.0')
