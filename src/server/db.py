import os
import psycopg2
from psycopg2.extras import execute_values
import humps
from problem import GenericProblem, ProblemProps
from query import Query

def getConnection():
  conn = psycopg2.connect(
    host=(os.environ['POSTGRES_HOST']
      if 'POSTGRES_HOST' in os.environ
      else 'localhost'),
    database="postgres",
    user=(os.environ['POSTGRES_USER']
      if 'POSTGRES_USER' in os.environ
      else 'postgres'),
    password=(os.environ['POSTGRES_PASSWORD']
      if 'POSTGRES_PASSWORD' in os.environ
      else 'v^oOB1uiZ7ylo$XbuYKDe$cnUKX9U0c0N9$r')
  )
  return conn

def getProblem(problem: GenericProblem):
  conn = getConnection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  cur.execute("""
  SELECT * FROM problems WHERE
    active_constraints = %s AND
    passive_constraints = %s AND
    leaf_constraints = %s AND
    root_constraints = %s AND
    
    is_tree = %s AND
    is_cycle = %s AND
    is_path = %s AND
    is_directed = %s AND
    is_rooted = %s AND
    is_regular = %s;
  """, (
    list(problem.activeConstraints),
    list(problem.passiveConstraints),
    list(problem.leafConstraints),
    list(problem.rootConstraints),

    problem.flags.isTree,
    problem.flags.isCycle,
    problem.flags.isPath,
    problem.flags.isDirected,
    problem.flags.isRooted,
    problem.flags.isRegular
  ))
  res = cur.fetchone()
  if res is not None:
    res = humps.camelize(res)
  
  cur.close()
  conn.close()

  return res

def getProblems(
  query: Query
):
  conn = getConnection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  cur.execute("""
  SELECT * FROM problems WHERE
    active_degree = %s AND
    passive_degree = %s AND
    label_count = %s AND
    actives_all_same = %s AND
    passives_all_same = %s AND

    rand_upper_bound <= %s AND
    rand_lower_bound >= %s AND
    det_upper_bound <= %s AND
    det_lower_bound >= %s AND

    (
      %s <@ active_constraints OR
      %s <@ passive_constraints
    ) AND

    (
      %s = '{}' OR
      (
        %s && active_constraints OR
        %s && passive_constraints
      )
    ) AND

    (
      %s = '{}' OR
      NOT (
        %s <@ active_constraints OR
        %s <@ passive_constraints
      )
    ) AND

    NOT (
      %s && active_constraints OR
      %s && passive_constraints
    ) AND
    
    is_tree = %s AND
    is_cycle = %s AND
    is_path = %s AND
    is_directed = %s AND
    is_rooted = %s AND
    is_regular = %s;
  """, (
    query.props.activeDegree,
    query.props.passiveDegree,
    query.props.labelCount,
    query.props.activesAllSame,
    query.props.passivesAllSame,

    query.bounds.randUpperBound,
    query.bounds.randLowerBound,
    query.bounds.detUpperBound,
    query.bounds.detLowerBound,

    query.excludeInclude.includeIfConfigHasAllOf,
    query.excludeInclude.includeIfConfigHasAllOf,

    query.excludeInclude.includeIfConfigHasSomeOf,
    query.excludeInclude.includeIfConfigHasSomeOf,
    query.excludeInclude.includeIfConfigHasSomeOf,

    query.excludeInclude.excludeIfConfigHasAllOf,
    query.excludeInclude.excludeIfConfigHasAllOf,
    query.excludeInclude.excludeIfConfigHasAllOf,
    
    query.excludeInclude.excludeIfConfigHasSomeOf,
    query.excludeInclude.excludeIfConfigHasSomeOf,

    query.props.flags.isTree,
    query.props.flags.isCycle,
    query.props.flags.isPath,
    query.props.flags.isDirected,
    query.props.flags.isRooted,
    query.props.flags.isRegular
  ))
  res = cur.fetchall()
  res = humps.camelize(res)
  
  cur.close()
  conn.close()

  if query.excludeInclude.returnSmallestProblemOnly:
    res = [min(
      res,
      key = lambda p: len(p['activeConstraints']) +
        len(p['passiveConstraints'])
    )]
  elif query.excludeInclude.returnLargestProblemOnly:
    res = [max(
      res,
      key = lambda p: len(p['activeConstraints']) +
        len(p['passiveConstraints'])
    )]
  return res

def updateClassifications(results):
  conn = getConnection()
  cur = conn.cursor()
  execute_values(cur, """
    UPDATE problems SET 
      rand_upper_bound = CAST (data.rand_upper_bound AS complexity),
      rand_lower_bound = CAST (data.rand_lower_bound AS complexity),
      det_upper_bound = CAST (data.det_upper_bound AS complexity),
      det_lower_bound = CAST (data.det_lower_bound AS complexity),
      solvable_count = data.solvable_count,
      unsolvable_count = data.unsolvable_count
    FROM (VALUES %s) AS data (
      id,
      rand_upper_bound,
      rand_lower_bound,
      det_upper_bound,
      det_lower_bound,
      solvable_count,
      unsolvable_count
    ) WHERE problems.id = data.id;""",
    [(
      p.problem.id,
      p.randUpperBound,
      p.randLowerBound,
      p.detUpperBound,
      p.detLowerBound,
      p.solvableCount,
      p.unsolvableCount
    ) for p in results]
  )
  conn.commit()
  cur.close()
  conn.close()

def storeProblemsAndGetWithIds(
  problems,
  problemProps: ProblemProps
):
  conn = getConnection()
  cur = conn.cursor()
  cur.execute("""
  DELETE FROM problems WHERE
    active_degree = %s AND
    passive_degree = %s AND
    label_count = %s AND
    actives_all_same = %s AND
    passives_all_same = %s AND
    is_tree = %s AND
    is_cycle = %s AND
    is_path = %s AND
    is_directed = %s AND
    is_rooted = %s AND
    is_regular = %s;
  """, (
    problemProps.activeDegree,
    problemProps.passiveDegree,
    problemProps.labelCount,
    problemProps.activesAllSame,
    problemProps.passivesAllSame,
    problemProps.flags.isTree,
    problemProps.flags.isCycle,
    problemProps.flags.isPath,
    problemProps.flags.isDirected,
    problemProps.flags.isRooted,
    problemProps.flags.isRegular
  ))
  ids = execute_values(cur, """
    INSERT INTO problems (
      active_degree,
      passive_degree,
      label_count,
      actives_all_same,
      passives_all_same,

      active_constraints,
      passive_constraints,
      root_constraints,
      leaf_constraints,
      is_tree,
      is_cycle,
      is_path,
      is_directed,
      is_rooted,
      is_regular
    ) VALUES %s RETURNING id;""",
    [(
        problemProps.activeDegree,
        problemProps.passiveDegree,
        problemProps.labelCount,
        problemProps.activesAllSame,
        problemProps.passivesAllSame,
        
        list(p.activeConstraints),
        list(p.passiveConstraints),
        list(p.leafConstraints),
        list(p.rootConstraints),
        p.flags.isTree,
        p.flags.isCycle,
        p.flags.isPath,
        p.flags.isDirected,
        p.flags.isRooted,
        p.flags.isRegular
      ) for p in problems],
      fetch=True
  )
  conn.commit()
  cur.close()
  conn.close()

  for i, p in enumerate(problems):
    p.id = ids[i]
  return problems
