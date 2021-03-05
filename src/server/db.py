import os
import psycopg2
from psycopg2.extras import execute_values
import humps
from problem import GenericProblem, ProblemProps
from config_util import eachConstrIsHomogeneous
from db_data_converter import mapToClassifiedProblem
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
      else 'mysecretpassword')
  )
  return conn

def getProblem(problem: GenericProblem):
  conn = getConnection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  cur.execute("""
  SELECT
    problems.*,
    rub.short_name AS rub_source_short_name,
    rub.name AS rub_source_name,
    rub.urls AS rub_source_urls,
    rlb.short_name AS rlb_source_short_name,
    rlb.name AS rlb_source_name,
    rlb.urls AS rlb_source_urls,
    dub.short_name AS dub_source_short_name,
    dub.name AS dub_source_name,
    dub.urls AS dub_source_urls,
    dlb.short_name AS dlb_source_short_name,
    dlb.name AS dlb_source_name,
    dlb.urls AS dlb_source_urls
  FROM problems
  LEFT OUTER JOIN sources AS rub
  ON (rand_upper_bound_source = rub.id)
  LEFT OUTER JOIN sources AS rlb
  ON (rand_lower_bound_source = rlb.id)
  LEFT OUTER JOIN sources AS dub
  ON (det_upper_bound_source = dub.id)
  LEFT OUTER JOIN sources AS dlb
  ON (det_lower_bound_source = dlb.id)
  WHERE
    active_constraints = %s AND
    passive_constraints = %s AND
    leaf_constraints = %s AND
    root_constraints = %s AND
    
    is_tree = %s AND
    is_cycle = %s AND
    is_path = %s AND
    is_directed_or_rooted = %s AND
    is_regular = %s;
  """, (
    list(problem.activeConstraints),
    list(problem.passiveConstraints),
    list(problem.leafConstraints),
    list(problem.rootConstraints),

    problem.flags.isTree,
    problem.flags.isCycle,
    problem.flags.isPath,
    problem.flags.isDirectedOrRooted,
    problem.flags.isRegular
  ))
  res = cur.fetchone()
  if res is not None:
    res = humps.camelize(res)
  
  cur.close()
  conn.close()

  return res

def getClassifiedProblemObj(problem: GenericProblem):
  r = getProblem(problem)
  return mapToClassifiedProblem(r) if r is not None else None

def getProblems(
  query: Query
):
  conn = getConnection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  cur.execute("""
  SELECT
    problems.*,
    rub.short_name AS rub_source_short_name,
    rub.name AS rub_source_name,
    rub.urls AS rub_source_urls,
    rlb.short_name AS rlb_source_short_name,
    rlb.name AS rlb_source_name,
    rlb.urls AS rlb_source_urls,
    dub.short_name AS dub_source_short_name,
    dub.name AS dub_source_name,
    dub.urls AS dub_source_urls,
    dlb.short_name AS dlb_source_short_name,
    dlb.name AS dlb_source_name,
    dlb.urls AS dlb_source_urls
  FROM problems
  LEFT OUTER JOIN sources AS rub
  ON (rand_upper_bound_source = rub.id)
  LEFT OUTER JOIN sources AS rlb
  ON (rand_lower_bound_source = rlb.id)
  LEFT OUTER JOIN sources AS dub
  ON (det_upper_bound_source = dub.id)
  LEFT OUTER JOIN sources AS dlb
  ON (det_lower_bound_source = dlb.id)
  WHERE
    active_degree = %s AND
    passive_degree = %s AND
    label_count = %s AND
    (
      actives_all_same = %s OR
      actives_all_same = true
    ) AND
    (
      passives_all_same = %s OR
      passives_all_same = true
    ) AND

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
    is_directed_or_rooted = %s AND
    is_regular = %s AND
    
    (
      %s = false OR
      (
        rand_upper_bound = '(n)' AND
        rand_lower_bound = '(1)'
      )
    ) AND
    
    (
      %s = false OR
      (
        rand_upper_bound != rand_lower_bound
      )
    ) AND

    (
      %s = false OR
      (
        det_upper_bound = '(n)' AND
        det_lower_bound = '(1)'
      )
    ) AND
    
    (
      %s = false OR
      (
        det_upper_bound != det_lower_bound
      )
    );
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

    list(query.excludeInclude.includeIfConfigHasAllOf),
    list(query.excludeInclude.includeIfConfigHasAllOf),

    list(query.excludeInclude.includeIfConfigHasSomeOf),
    list(query.excludeInclude.includeIfConfigHasSomeOf),
    list(query.excludeInclude.includeIfConfigHasSomeOf),

    list(query.excludeInclude.excludeIfConfigHasAllOf),
    list(query.excludeInclude.excludeIfConfigHasAllOf),
    list(query.excludeInclude.excludeIfConfigHasAllOf),
    
    list(query.excludeInclude.excludeIfConfigHasSomeOf),
    list(query.excludeInclude.excludeIfConfigHasSomeOf),

    query.props.flags.isTree,
    query.props.flags.isCycle,
    query.props.flags.isPath,
    query.props.flags.isDirectedOrRooted,
    query.props.flags.isRegular,

    query.excludeInclude.completelyRandUnclassifedOnly,
    query.excludeInclude.partiallyRandUnclassifiedOnly,
    query.excludeInclude.completelyDetUnclassifedOnly,
    query.excludeInclude.partiallyDetUnclassifiedOnly
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

def getClassifiedProblemObjs(
  query: Query
):
  res = getProblems(query)
  return [mapToClassifiedProblem(r) for r in res]

def insertBatchClassifyTrace(
  cur,
  problemProps,
  problemCount
):
   cur.execute("""
      INSERT INTO batch_classifications (
        active_degree,
        passive_degree,
        label_count,
        actives_all_same,
        passives_all_same,

        is_tree,
        is_cycle,
        is_path,
        is_directed_or_rooted,
        is_regular,

        count
      ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s
      );""",
      (
        problemProps.activeDegree,
        problemProps.passiveDegree,
        problemProps.labelCount,
        problemProps.activesAllSame,
        problemProps.passivesAllSame,

        problemProps.flags.isTree,
        problemProps.flags.isCycle,
        problemProps.flags.isPath,
        problemProps.flags.isDirectedOrRooted,
        problemProps.flags.isRegular,

        problemCount
      )
    )
def updateClassifications(results, problemProps = None):
  conn = getConnection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  cur.execute("SELECT * FROM sources;")
  sources = cur.fetchall()
  sourcesMap = {s['short_name']: s['id'] for s in sources}

  execute_values(cur, """
    UPDATE problems SET 
      rand_upper_bound = CAST (data.rand_upper_bound AS complexity),
      rand_lower_bound = CAST (data.rand_lower_bound AS complexity),
      det_upper_bound = CAST (data.det_upper_bound AS complexity),
      det_lower_bound = CAST (data.det_lower_bound AS complexity),
      solvable_count = data.solvable_count,
      unsolvable_count = data.unsolvable_count,

      rand_upper_bound_source = data.rub_source,
      rand_lower_bound_source = data.rlb_source,
      det_upper_bound_source = data.dub_source,
      det_lower_bound_source = data.dlb_source
    FROM (VALUES %s) AS data (
      id,
      rand_upper_bound,
      rand_lower_bound,
      det_upper_bound,
      det_lower_bound,
      solvable_count,
      unsolvable_count,

      rub_source,
      rlb_source,
      dub_source,
      dlb_source
    ) WHERE problems.id = data.id;""",
    [(
      p.problem.id,
      p.randUpperBound,
      p.randLowerBound,
      p.detUpperBound,
      p.detLowerBound,
      p.solvableCount,
      p.unsolvableCount,
      
      sourcesMap[p.papers.getRUBSource()],
      sourcesMap[p.papers.getRLBSource()],
      sourcesMap[p.papers.getDUBSource()],
      sourcesMap[p.papers.getDLBSource()]
    ) for p in results]
  )

  if problemProps is not None:
    insertBatchClassifyTrace(
      cur,
      problemProps,
      len(results)
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
    (
      actives_all_same = %s OR
      actives_all_same = true
    ) AND
    (
      passives_all_same = %s OR
      passives_all_same = true 
    ) AND
    is_tree = %s AND
    is_cycle = %s AND
    is_path = %s AND
    is_directed_or_rooted = %s AND
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
    problemProps.flags.isDirectedOrRooted,
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
      is_directed_or_rooted,
      is_regular
    ) VALUES %s RETURNING id;""",
    [(
        problemProps.activeDegree,
        problemProps.passiveDegree,
        problemProps.labelCount,
        (
          problemProps.activesAllSame or
          eachConstrIsHomogeneous(p.activeConstraints)
        ),
        (
          problemProps.passivesAllSame or
          eachConstrIsHomogeneous(p.passiveConstraints)
        ),
        list(p.activeConstraints),
        list(p.passiveConstraints),
        list(p.leafConstraints),
        list(p.rootConstraints),
        p.flags.isTree,
        p.flags.isCycle,
        p.flags.isPath,
        p.flags.isDirectedOrRooted,
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

def getBatchClassifications():
  conn = getConnection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  cur.execute("SELECT * FROM batch_classifications;")
  res = cur.fetchall()
  cur.close()
  conn.close()

  return res

def getProblemCount():
  conn = getConnection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  cur.execute("SELECT COUNT(*) as count FROM problems;")
  res = cur.fetchone()
  cur.close()
  conn.close()

  return res['count']

