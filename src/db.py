import psycopg2
from psycopg2.extras import execute_values
import humps
from problem import ProblemProps
from query import Query

def getConnection():
  conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mysecretpassword"
  )
  return conn

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

    query.props.flags.isTree,
    query.props.flags.isCycle,
    query.props.flags.isPath,
    query.props.flags.isDirected,
    query.props.flags.isRooted,
    query.props.flags.isRegular
  ))
  res = cur.fetchall()  
  res = humps.camelize(res)
  # print(res[21])
  
  cur.close()
  conn.close()
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
        
        " ".join(p.activeConstraints),
        " ".join(p.passiveConstraints),
        " ".join(p.leafConstraints),
        " ".join(p.rootConstraints),
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
