from common.db import get_project_conn,OLLAMA_URL,MODEL_NAME
from pages.leader.services.project_detail_service import (
    get_project_progress_list
)
from pages.leader.services.ai_business_service import call_llm

from pages.leader.services.task_center.task_center_service import (
    get_user_tasks
)

#新增查询员工项目
def get_user_projects(username):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select
            p.id,
            p.project_name
        from project_member m
        left join project p
        on m.project_id=p.id
        where m.username=?
        """,
        (username,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def build_my_project_html(real_name):

    rows = get_user_project_dashboard(
        real_name
    )

    if not rows:
        return """
        <div class="empty-card">
            暂无参与项目
        </div>
        """

    html = """
    <div class="project-grid">
    """

    for item in rows:

        try:
            progress = int(item["progress"])
        except:
            progress = 0

        if progress >= 80:
            health = 95
        elif progress >= 50:
            health = 85
        else:
            health = 70

        risk_index = item["risk_count"]

        html += f"""

        <div
            class="project-dashboard-card"
            onclick="openMyProject('{item['id']}')"
        >

            <div class="project-header">

                <div>

                    <div class="project-title">

                        📁 {item['project_name']}

                    </div>

                    <div class="project-leader">

                        负责人：{item['leader']}
                    </div>

                </div>

                <div class="health-tag">

                    健康度 {health}

                </div>

            </div>

            <div class="project-stat-row">

                <span>
                    👥 {item['member_count']}人
                </span>

                <span>
                    ⚠ {item['risk_count']}项风险
                </span>

                <span>
                    📈 {item['progress_count']}条进展
                </span>

            </div>

            <div class="progress-wrap">

                <div class="progress-label">

                    项目进度

                    <span>
                        {progress}%
                    </span>

                </div>

                <div class="progress-bar">

                    <div
                        class="progress-inner"
                        style="width:{progress}%"
                    ></div>

                </div>

            </div>

            <div class="project-footer">

                风险指数：{risk_index}

            </div>

        </div>
        """

    html += "</div>"

    return html

def add_my_project_progress(
        project_id,
        reporter,
        progress_content,
        risk_content,
        next_plan
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        insert into project_progress(

            project_id,
            progress_date,
            progress_content,
            risk_content,
            next_plan,
            reporter

        )

        values(

            ?,
            datetime('now'),
            ?,
            ?,
            ?,
            ?

        )
        """,
        (
            project_id,
            progress_content,
            risk_content,
            next_plan,
            reporter
        )
    )

    conn.commit()

    conn.close()

    return "✅ 项目进展提交成功"


def get_my_project_progress(
        project_id,
        reporter
):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select

            id,
            progress_date,
            progress_content,
            risk_content,
            next_plan

        from project_progress

        where project_id=?
        and reporter=?

        order by id desc
        """,
        (
            project_id,
            reporter
        )
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def build_my_project_progress_html(
        project_id,
        reporter
):
    rows = get_my_project_progress(
        project_id,
        reporter
    )
    html = ""
    for row in rows:
        html += f"""
        <div class='progress-card'>
            <div>
                <b>{row[1]}</b>
            </div>
            <div>
                {row[2]}
            </div>
            <div>
                风险：
                {row[3]}
            </div>
            <div>
                下一步：
                {row[4]}
            </div>
            <div
                style="
                    margin-top:10px;
                "
            >
                <button
                    class="edit-btn"
                    onclick="editMyProgress('{row[0]}')"
                >
                    编辑
                </button>

                <button
                    class="delete-btn"
                    onclick="deleteMyProgress('{row[0]}')"
                >
                    删除
                </button>
            </div>
        </div>
        """
    return html

def delete_my_progress(progress_id):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        delete from project_progress
        where id=?
        """,
        (progress_id,)
    )
    conn.commit()
    conn.close()
    return True

def delete_progress_and_refresh(
        progress_id,
        project_id,
        reporter
):

    delete_my_progress(
        progress_id
    )
    return build_my_project_progress_html(
        project_id,
        reporter
    )

def get_progress_detail(progress_id):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select

            progress_content,
            risk_content,
            next_plan

        from project_progress
        where id=?
        """,
        (progress_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row

def load_my_progress(progress_id):
    row = get_progress_detail(
        progress_id
    )
    if not row:
        return (
            "",
            "",
            ""
        )
    return (
        row[0],
        row[1],
        row[2]
    )

def update_my_progress(
        progress_id,
        progress_content,
        risk_content,
        next_plan
):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        update project_progress
        set

            progress_content=?,
            risk_content=?,
            next_plan=?

        where id=?
        """,
        (
            progress_content,
            risk_content,
            next_plan,
            progress_id
        )
    )
    conn.commit()
    conn.close()
    return "✅ 修改成功"

#刷新函数
def update_progress_and_refresh(
        progress_id,
        project_id,
        reporter,
        progress_content,
        risk_content,
        next_plan
):

    update_my_progress(
        progress_id,
        progress_content,
        risk_content,
        next_plan
    )

    return build_my_project_progress_html(
        project_id,
        reporter
    )

#新增统计函数
def get_my_project_stat(project_id):

    conn = get_project_conn()

    cur = conn.cursor()

    # 进展数量
    cur.execute(
        """
        select count(*)
        from project_progress
        where project_id=?
        """,
        (project_id,)
    )

    progress_count = cur.fetchone()[0]

    # 风险数量
    cur.execute(
        """
        select count(*)
        from project_risk
        where project_id=?
        """,
        (project_id,)
    )

    risk_count = cur.fetchone()[0]

    # 最近更新时间
    cur.execute(
        """
        select progress_date
        from project_progress
        where project_id=?
        order by id desc
        limit 1
        """,
        (project_id,)
    )

    row = cur.fetchone()

    last_update = "-"

    if row:
        last_update = row[0]

    conn.close()

    return {
        "progress": progress_count,
        "risk": risk_count,
        "last_update": last_update
    }

#生成统计卡片
def build_my_project_kpi_html(project_id):
    stat = get_my_project_stat(
        project_id
    )
    return f"""
    <div class="project-stat-wrap">
        <div class="stat-card">
            项目进展
            <br>
            {stat["progress"]}
        </div>
        <div class="stat-card">
            风险数量
            <br>
            {stat["risk"]}
        </div>
        <div class="stat-card">
            最近更新
            <br>
            {stat["last_update"]}
        </div>
    </div>
    """

def build_my_project_ai_analysis(project_id):

    progress_rows = get_project_progress_list(
        project_id
    )

    prompt = f"""
你是项目管理顾问。

请根据项目进展分析：

1 项目当前状态

2 当前风险

3 是否存在延期风险

4 下一阶段建议

项目进展：

{progress_rows}

"""

    return call_llm(prompt)

def get_user_project_dashboard(username):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM project
    WHERE

        main_leader=?

        OR developers LIKE ?

        OR testers LIKE ?

        OR designer LIKE ?

        OR structure_engineer LIKE ?

    ORDER BY id DESC
    """,
    (
        username,
        f"%{username}%",
        f"%{username}%",
        f"%{username}%",
        f"%{username}%"
    ))

    rows = cur.fetchall()

    result = []

    print("查询用户=", username)
    print("查询结果=", rows)
    for row in rows:

        result.append({

            "id": row[0],

            "project_name": row[1],

            "leader": row[3],

            "progress": 50,

            "member_count": len(
                ",".join([
                    row[9] or "",
                    row[10] or "",
                    row[11] or "",
                    row[12] or ""
                ]).split(",")
            ),

            "risk_count": 0,

            "progress_count": 0

        })

    conn.close()

    return result

def get_my_project_summary(username):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT count(*)
    FROM project
    WHERE

        main_leader=?

        OR developers LIKE ?

        OR testers LIKE ?

        OR designer LIKE ?

        OR structure_engineer LIKE ?
    """,
    (
        username,
        f"%{username}%",
        f"%{username}%",
        f"%{username}%",
        f"%{username}%"
    ))

    total = cur.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "running": total,
        "high_risk": 0,
        "finished": 0
    }

def build_my_project_summary_html(real_name):
    stat = get_my_project_summary(
        real_name
    )
    return f"""
    <div class="my-project-summary">
        <div class="summary-card">
            <div class="summary-value">
                {stat["total"]}
            </div>
            <div class="summary-label">
                我的项目
            </div>
        </div>
        <div class="summary-card">
            <div class="summary-value">
                {stat["running"]}
            </div>
            <div class="summary-label">
                进行中
            </div>
        </div>
        <div class="summary-card">
            <div class="summary-value">
                {stat["high_risk"]}
            </div>
            <div class="summary-label">
                高风险
            </div>
        </div>
        <div class="summary-card">
            <div class="summary-value">
                {stat["finished"]}
            </div>
            <div class="summary-label">
                已完成
            </div>
        </div>
    </div>
    """

def query_project_info(project_name):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute("""
    select
        main_leader,
        developers,
        testers,
        designer,
        structure_engineer,
        start_date,
        end_date
    from project
    where project_name=?
    limit 1
    """,(project_name,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return "", "", "", ""
    members = []
    for v in row[1:5]:
        if v:
            members.append(v)
    return (
        row[0],
        row[5],
        row[6],
        ",".join(members)
    )

def query_my_project(username):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM project
    WHERE
        main_leader=?
        OR developers LIKE ?
        OR testers LIKE ?
        OR designer LIKE ?
        OR structure_engineer LIKE ?
    """,
    (
        username,
        f"%{username}%",
        f"%{username}%",
        f"%{username}%",
        f"%{username}%"
    ))

    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append({

            "id": row[0],

            "project_name": row[1],

            "leader": row[3],

            "progress": row[7] or "0",

            "delay": row[5] or "否",

            "member_count":
                len(
                    ",".join([
                        row[9] or "",
                        row[10] or "",
                        row[11] or "",
                        row[12] or ""
                    ]).split(",")
                ),

            "risk_count":
                1 if (row[6] or "").strip() else 0,

            "progress_count":
                1

        })

    return result

def build_task_html(
        username
):

    tasks = get_user_tasks(
        username
    )

    html = ""

    for t in tasks:

        html += f"""
        <div class='todo-card'>

            <b>{t[1]}</b>

            <br>

            优先级：

            {t[2]}

            <br>

            截止：

            {t[3]}

        </div>
        """

    return html