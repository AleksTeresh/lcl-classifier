import psycopg2
from psycopg2.extras import execute_values
from problem import ProblemProps
from complexity import complexityToInt

def getConnection():
  conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mysecretpassword"
  )
  return conn

def updateClassifications(results):
  conn = getConnection()
  cur = conn.cursor()
  execute_values(cur, """
    UPDATE problems SET 
      rand_upper_bound = data.rand_upper_bound,
      rand_lower_bound = data.rand_lower_bound,
      det_upper_bound = data.det_upper_bound,
      det_lower_bound = data.det_lower_bound,
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
      complexityToInt[p.randUpperBound],
      complexityToInt[p.randLowerBound],
      complexityToInt[p.detUpperBound],
      complexityToInt[p.detLowerBound],
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
