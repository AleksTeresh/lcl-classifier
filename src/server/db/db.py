import os
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from typing import List, Dict, Optional
from psycopg2.extras import execute_values
from problem import GenericProblem, ProblemProps
from response import GenericResponse
from problem import each_constr_is_homogeneous
from .db_data_converter import map_to_classified_problem
from .classified_problem import ClassifiedProblem
from query import Query

_connection_pool = None


def get_connection_pool():
    # needed to avoid "local variable referenced before assignment" error
    # see e.g. https://vbsreddy1.medium.com/unboundlocalerror-when-the-variable-has-a-value-in-python-e34e097547d6
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = psycopg2.pool.SimpleConnectionPool(
            1,
            20,
            host=(
                os.environ["POSTGRES_HOST"]
                if "POSTGRES_HOST" in os.environ
                else "localhost"
            ),
            database="postgres",
            user=(
                os.environ["POSTGRES_USER"]
                if "POSTGRES_USER" in os.environ
                else "postgres"
            ),
            password=(
                os.environ["POSTGRES_PASSWORD"]
                if "POSTGRES_PASSWORD" in os.environ
                else "mysecretpassword"
            ),
        )
    return _connection_pool


# the function is copied from https://medium.com/@thegavrikstory/manage-raw-database-connection-pool-in-flask-b11e50cbad3
@contextmanager
def get_connection():
    pool = get_connection_pool()
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


# the function is copied from https://medium.com/@thegavrikstory/manage-raw-database-connection-pool-in-flask-b11e50cbad3


@contextmanager
def get_db_cursor(commit=False):
    with get_connection() as connection:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            yield cursor
            if commit:
                connection.commit()
        finally:
            cursor.close()


def get_problem(problem: GenericProblem) -> Optional[Dict]:
    with get_db_cursor() as cur:
        cur.execute(
            """
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
    """,
            (
                list(problem.active_constraints),
                list(problem.passive_constraints),
                list(problem.leaf_constraints),
                list(problem.root_constraints),
                problem.flags.is_tree,
                problem.flags.is_cycle,
                problem.flags.is_path,
                problem.flags.is_directed_or_rooted,
                problem.flags.is_regular,
            ),
        )
        res = cur.fetchone()

    return res


def get_classified_problem_obj(problem: GenericProblem) -> Optional[ClassifiedProblem]:
    r = get_problem(problem)
    return map_to_classified_problem(r) if r is not None else None


def get_problems(query: Query) -> List[Dict]:
    with get_db_cursor() as cur:
        cur.execute(
            """
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
            """,
            (
                query.props.active_degree,
                query.props.passive_degree,
                query.props.label_count,
                query.props.actives_all_same,
                query.props.passives_all_same,
                query.bounds.rand_upper_bound,
                query.bounds.rand_lower_bound,
                query.bounds.det_upper_bound,
                query.bounds.det_lower_bound,
                list(query.exclude_include.include_if_config_has_all_of),
                list(query.exclude_include.include_if_config_has_all_of),
                list(query.exclude_include.include_if_config_has_some_of),
                list(query.exclude_include.include_if_config_has_some_of),
                list(query.exclude_include.include_if_config_has_some_of),
                list(query.exclude_include.exclude_if_config_has_all_of),
                list(query.exclude_include.exclude_if_config_has_all_of),
                list(query.exclude_include.exclude_if_config_has_all_of),
                list(query.exclude_include.exclude_if_config_has_some_of),
                list(query.exclude_include.exclude_if_config_has_some_of),
                query.props.flags.is_tree,
                query.props.flags.is_cycle,
                query.props.flags.is_path,
                query.props.flags.is_directed_or_rooted,
                query.props.flags.is_regular,
                query.exclude_include.completely_rand_unclassifed_only,
                query.exclude_include.partially_rand_unclassified_only,
                query.exclude_include.completely_det_unclassifed_only,
                query.exclude_include.partially_det_unclassified_only,
            ),
        )
        res = cur.fetchall()

        if len(res) == 0:
            return res
        else:
            if query.exclude_include.return_smallest_problem_only:
                res = [
                    min(
                        res,
                        key=lambda p: len(p["active_constraints"])
                        + len(p["passive_constraints"]),
                    )
                ]
            elif query.exclude_include.return_largest_problem_only:
                res = [
                    max(
                        res,
                        key=lambda p: len(p["active_constraints"])
                        + len(p["passive_constraints"]),
                    )
                ]
            return res


def get_classified_problem_objs(query: Query) -> List[ClassifiedProblem]:
    res = get_problems(query)
    return [map_to_classified_problem(r) for r in res]


def insert_batch_classify_trace(
    cur,
    problem_props: ProblemProps,
    problem_count: int,
    count_limit: Optional[int],
    skip_count: Optional[int],
) -> None:
    cur.execute(
        """
      DELETE FROM batch_classifications WHERE
       (
          active_degree = %s AND
          passive_degree = %s AND
          label_count = %s AND
          actives_all_same = %s AND
          passives_all_same = %s AND

          is_tree = %s AND
          is_cycle = %s AND
          is_path = %s AND
          is_directed_or_rooted = %s AND
          is_regular = %s
       );
      """,
        (
            problem_props.active_degree,
            problem_props.passive_degree,
            problem_props.label_count,
            problem_props.actives_all_same,
            problem_props.passives_all_same,
            problem_props.flags.is_tree,
            problem_props.flags.is_cycle,
            problem_props.flags.is_path,
            problem_props.flags.is_directed_or_rooted,
            problem_props.flags.is_regular,
        ),
    )
    cur.execute(
        """
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

        count,
        count_limit,
        skip_count
      ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s
      ) RETURNING id;""",
        (
            problem_props.active_degree,
            problem_props.passive_degree,
            problem_props.label_count,
            problem_props.actives_all_same,
            problem_props.passives_all_same,
            problem_props.flags.is_tree,
            problem_props.flags.is_cycle,
            problem_props.flags.is_path,
            problem_props.flags.is_directed_or_rooted,
            problem_props.flags.is_regular,
            problem_count,
            count_limit,
            0 if skip_count is None else skip_count,
        ),
    )


def get_batchless_problems() -> List[Dict]:
    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT * FROM problems WHERE batch_id = NULL;")
        problems = cur.fetchall()

        return problems


def get_batchless_problem_objs() -> List[ClassifiedProblem]:
    problems = get_batchless_problems()
    return [map_to_classified_problem(r) for r in problems]


def store_problem_and_classification(
    problem: GenericProblem, response: GenericResponse
) -> None:
    problem_id = store_problem(problem)
    update_classification(response, problem_id)


def update_classification(result: GenericResponse, problem_id: int) -> None:
    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT * FROM sources;")
        sources = cur.fetchall()
        sources_map = {s["short_name"]: s["id"] for s in sources}

        cur.execute(
            """
            UPDATE problems SET 
            rand_upper_bound = CAST (%s AS complexity),
            rand_lower_bound = CAST (%s AS complexity),
            det_upper_bound = CAST (%s AS complexity),
            det_lower_bound = CAST (%s AS complexity),
            solvable_count = %s,
            unsolvable_count = %s,

            rand_upper_bound_source = %s,
            rand_lower_bound_source = %s,
            det_upper_bound_source = %s,
            det_lower_bound_source = %s
            WHERE problems.id = %s;""",
            (
                result.rand_upper_bound,
                result.rand_lower_bound,
                result.det_upper_bound,
                result.det_lower_bound,
                result.solvable_count,
                result.unsolvable_count,
                sources_map[result.papers.get_rub_source()],
                sources_map[result.papers.get_rlb_source()],
                sources_map[result.papers.get_dub_source()],
                sources_map[result.papers.get_dlb_source()],
                problem_id,
            ),
        )


def update_classifications(
    results: List[GenericResponse],
    problem_props=None,
    count_limit=None,
    skip_count=None,
) -> None:
    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT * FROM sources;")
        sources = cur.fetchall()
        sources_map = {s["short_name"]: s["id"] for s in sources}

        print("Updating classification data...")
        execute_values(
            cur,
            """
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
            [
                (
                    p.problem.id,
                    p.rand_upper_bound,
                    p.rand_lower_bound,
                    p.det_upper_bound,
                    p.det_lower_bound,
                    p.solvable_count,
                    p.unsolvable_count,
                    sources_map[p.papers.get_rub_source()],
                    sources_map[p.papers.get_rlb_source()],
                    sources_map[p.papers.get_dub_source()],
                    sources_map[p.papers.get_dlb_source()],
                )
                for p in results
            ],
        )

        if problem_props is not None:
            insert_batch_classify_trace(
                cur, problem_props, len(results), count_limit, skip_count
            )
            batch_id = cur.fetchone()["id"]
            execute_values(
                cur,
                """
            UPDATE problems SET
                batch_id = data.batch_id
            FROM (VALUES %s) AS data (
                batch_id,
                problem_id
            )
            WHERE problems.id = data.problem_id;""",
                [(batch_id, p.problem.id) for p in results],
            )


def store_problem(p: GenericProblem) -> int:
    r = get_problem(p)

    with get_db_cursor(commit=True) as cur:
        if r is not None:
            cur.execute("DELETE FROM problems WHERE id = %s", [r["id"]])

        cur.execute(
            """
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
        ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s
        ) RETURNING id;""",
            (
                p.get_active_degree(),
                p.get_passive_degree(),
                len(p.get_alphabet()),
                each_constr_is_homogeneous(p.active_constraints),
                each_constr_is_homogeneous(p.passive_constraints),
                list(p.active_constraints),
                list(p.passive_constraints),
                list(p.leaf_constraints),
                list(p.root_constraints),
                p.flags.is_tree,
                p.flags.is_cycle,
                p.flags.is_path,
                p.flags.is_directed_or_rooted,
                p.flags.is_regular,
            ),
        )

        res = cur.fetchone()
        return res["id"]


def store_problems_and_get_with_ids(
    problems: List[GenericProblem], problem_props: ProblemProps
) -> List[GenericProblem]:
    with get_db_cursor(commit=True) as cur:
        cur.execute(
            """
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
            """,
            (
                problem_props.active_degree,
                problem_props.passive_degree,
                problem_props.label_count,
                problem_props.actives_all_same,
                problem_props.passives_all_same,
                problem_props.flags.is_tree,
                problem_props.flags.is_cycle,
                problem_props.flags.is_path,
                problem_props.flags.is_directed_or_rooted,
                problem_props.flags.is_regular,
            ),
        )
        idObjecets = execute_values(
            cur,
            """
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
            [
                (
                    problem_props.active_degree,
                    problem_props.passive_degree,
                    problem_props.label_count,
                    (
                        problem_props.actives_all_same
                        or each_constr_is_homogeneous(p.active_constraints)
                    ),
                    (
                        problem_props.passives_all_same
                        or each_constr_is_homogeneous(p.passive_constraints)
                    ),
                    list(p.active_constraints),
                    list(p.passive_constraints),
                    list(p.leaf_constraints),
                    list(p.root_constraints),
                    p.flags.is_tree,
                    p.flags.is_cycle,
                    p.flags.is_path,
                    p.flags.is_directed_or_rooted,
                    p.flags.is_regular,
                )
                for p in problems
            ],
            fetch=True,
        )

    for i, p in enumerate(problems):
        p.id = idObjecets[i]["id"]
    return problems


def get_batch_classifications() -> List[Dict]:
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM batch_classifications;")
        res = cur.fetchall()
        return res


def get_batch_classification_by_query(query: Query) -> List[Dict]:
    with get_db_cursor() as cur:
        cur.execute(
            """
            SELECT * FROM batch_classifications
            WHERE
            active_degree = %s AND
            passive_degree = %s AND
            label_count = %s AND
            (
                actives_all_same = %s OR
                actives_all_same = false
            ) AND
            (
                passives_all_same = %s OR
                passives_all_same = false
            ) AND

            is_tree = %s AND
            is_cycle = %s AND
            is_path = %s AND
            is_directed_or_rooted = %s AND
            is_regular = %s;
            """,
            (
                query.props.active_degree,
                query.props.passive_degree,
                query.props.label_count,
                query.props.actives_all_same,
                query.props.passives_all_same,
                query.props.flags.is_tree,
                query.props.flags.is_cycle,
                query.props.flags.is_path,
                query.props.flags.is_directed_or_rooted,
                query.props.flags.is_regular,
            ),
        )
        res = cur.fetchall()
        return [] if res is None else res


def get_problem_count() -> int:
    with get_db_cursor() as cur:
        cur.execute("SELECT COUNT(*) as count FROM problems;")
        res = cur.fetchone()

        return res["count"]
