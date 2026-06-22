from common.db import get_project_conn


def get_project_detail(project_id):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            project_name,
            main_leader,
            progress,
            is_delay,
            risk_block
        from project
        where id=?
        """,
        (project_id,)
    )

    row = cur.fetchone()

    conn.close()

    return row