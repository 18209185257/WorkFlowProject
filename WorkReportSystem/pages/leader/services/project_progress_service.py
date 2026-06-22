from common.db import get_project_conn
from datetime import datetime

def get_project_progress(project_id):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select

        progress_date,
        progress_content,
        risk_content,
        next_plan,
        reporter

    from project_progress

    where project_id=?

    order by progress_date desc
    """,(project_id,))

    rows = cur.fetchall()

    conn.close()

    return rows

def add_project_progress(
        project_id,
        progress_content,
        risk_content,
        next_plan,
        reporter
):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute("""
    insert into project_progress(
        project_id,
        progress_date,
        progress_content,
        risk_content,
        next_plan,
        reporter,
        create_time
    )
    values(?,?,?,?,?,?,?)
    """,(
        project_id,
        datetime.now().strftime(
            "%Y-%m-%d"
        ),
        progress_content,
        risk_content,
        next_plan,
        reporter,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))
    conn.commit()
    conn.close()

# 获取项目全部进展
def get_project_progress_full(project_id):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select

        id,
        progress_date,
        progress_content,
        risk_content,
        next_plan,
        reporter

    from project_progress

    where project_id=?

    order by id desc
    """,(project_id,))

    rows = cur.fetchall()

    conn.close()

    return rows

#更新进展
def update_project_progress(
        progress_id,
        progress_content,
        risk_content,
        next_plan
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    update project_progress

    set

        progress_content=?,
        risk_content=?,
        next_plan=?

    where id=?
    """,(

        progress_content,
        risk_content,
        next_plan,
        progress_id
    ))

    conn.commit()

    conn.close()

# 删除进展
def delete_project_progress(progress_id):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    delete from project_progress

    where id=?
    """,(progress_id,))

    conn.commit()

    conn.close()

def get_progress_by_id(progress_id):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute("""
    select

        id,
        progress_content,
        risk_content,
        next_plan

    from project_progress

    where id=?
    """,(progress_id,))
    row = cur.fetchone()
    conn.close()
    return row

def get_project_progress_list(project_id):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select

            id,
            reporter,
            progress_content,
            risk_content,
            next_plan,
            create_time
        from project_progress
        where project_id=?
        order by id desc
        """,
        (project_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def get_project_progress_for_ai(project_id):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select
            reporter,
            progress_content,
            risk_content,
            next_plan
        from project_progress
        where project_id=?
        order by id desc
        limit 50
        """,
        (project_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

