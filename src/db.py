import psycopg2
from psycopg2.extras import execute_values
from problem import ProblemProps

# def updateClassifications(
#   results
# )

def storeProblems(
  problems,
  problemProps: ProblemProps
):
  conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mysecretpassword"
  )
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
  execute_values(cur, """
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
    ) VALUES %s;""",
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
      ) for p in problems]
  )
  conn.commit()
  cur.close()
  conn.close()
