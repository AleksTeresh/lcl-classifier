import flask
from flask_restful import inputs
from flask import request, jsonify
from problem import GenericProblem, ProblemFlags
from classifier import classify
from db import getProblem

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/classifier/problem', methods=['GET'])
def problem():
    isTree = inputs.boolean(request.args.get('is_tree'))
    isCycle = inputs.boolean(request.args.get('is_cycle'))
    isPath = inputs.boolean(request.args.get('is_path'))
    isDirected = inputs.boolean(request.args.get('is_directed'))
    isRooted = inputs.boolean(request.args.get('is_rooted'))
    isRegular = inputs.boolean(request.args.get('is_regular'))

    activeConstraints = request.args.getlist('active_constraints')
    passiveConstraints = request.args.getlist('passive_constraints')
    leafConstraints = request.args.getlist('leaf_constraints')
    rootConstraints = request.args.getlist('root_constraints')

    p = GenericProblem(
      activeConstraints,
      passiveConstraints,
      leafConstraints,
      rootConstraints,
      leafAllowAll=(leafConstraints == []),
      rootAllowAll=(rootConstraints == []),
      flags=ProblemFlags(
        isTree=isTree,
        isCycle=isCycle,
        isPath=isPath,
        isDirected=isDirected,
        isRooted=isRooted,
        isRegular=isRegular,
      )
    )

    res = getProblem(p)
    if res is not None:
      return jsonify(res)
    else:
      res = classify(p)
      return jsonify(res.dict())

@app.route('/api/classifier/query', methods=['GET'])
def query():

    return "<h1>LCL classifier</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run()
