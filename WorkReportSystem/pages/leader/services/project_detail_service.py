from common.db import get_project_conn,OLLAMA_URL,MODEL_NAME
from .project_progress_service import (
    get_project_progress_full,
    get_project_progress
)
from .ai_business_service import call_llm
import requests
from common.config import (
    API_HOST,
    TOKEN
)

from .project_progress_service import (
    get_project_progress_list
)

def get_project_detail(project_id):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute("""
    select
        project_name,
        main_leader,
        project_cycle,
        progress,
        is_delay,
        risk_block
    from project
    where id=?
    """,(project_id,))
    row = cur.fetchone()
    conn.close()
    return row

def get_project_members(project_id):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select
            id,
            member_name,
            role_in_project
        from project_member
        where project_id=?
        order by id desc
        """,
        (project_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def get_project_risks(project_id):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute("""
    select
        risk_level,
        risk_content,
        solution
    from project_risk
    where project_id=?
    order by id desc
    """ , (project_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def build_project_detail_html(project_id):
    stat = get_project_statistics(project_id)
    health_score = calculate_health_score(project_id)
    risk_index = calculate_risk_index(project_id)
    detail = get_project_detail(project_id)
    members = get_project_members(project_id)
    progress_rows = get_project_progress_full(project_id)
    risks = get_project_risks(project_id)

    if not detail:
        return "<h3>项目不存在</h3>"
    member_html = ""
    for m in members:
        member_html += f"""
        <div class='member-card'>
        <span>
            {m[1]}
        </span>
        <span>
            {m[2]}
        </span>
        <button
            onclick="deleteMember('{m[0]}')"
        >
            删除
        </button>

    </div>
        """
    progress_html = ""

    for p in progress_rows:
        progress_id = p[0]
        progress_date = p[1]
        progress_content = p[2]
        risk_content = p[3]
        next_plan = p[4]
        reporter = p[5]
        progress_html += f"""
        
        <div class='project-stat-wrap'>
            <div class='stat-card'>
                成员数：{stat["member_count"]}
            </div>
            <div class='stat-card'>
                风险数：{stat["risk_count"]}
            </div>
            <div class='stat-card'>
                进展数：{stat["progress_count"]}
            </div>
            <div class="stat-card">
                健康度
                <br>     
               {health_score}
            </div>
            <div class="stat-card">
                风险指数
                <br>
               {risk_index}
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
                <div class="timeline-header">
                    <span>
                        {progress_date}
                    </span>
                    <span>
                        {reporter}
                    </span>
                </div>
                <div class="timeline-body">
                    <b>项目进展：</b>
                    {progress_content}
                    <br><br>
                    <b>风险：</b>
                    {risk_content}
                    <br><br>
                    <b>下一步：</b>
                    {next_plan}
                </div>
                <div
                    style="
                        margin-top:12px;
                    "
                >

                    <button
                    class="edit-btn"
                    onclick="editProjectProgress('{progress_id}')">
                    编辑
                    </button>

                    <button
                    class="delete-btn"
                    onclick="deleteProjectProgress('{progress_id}')">
                    删除
                    </button>
                </div>
            </div>
        </div>
        """

    risk_html = ""
    for r in risks:
        risk_html += f"""
        <div class='risk-card'>
            <b>{r[0]}</b>
            <br>
            {r[1]}
            <br>
            解决方案：
            {r[2]}
        </div>
        """

    risk_html = ""
    for r in risks:
        risk_html += f"""
        <div class='risk-card'>
            <div>
                <b>{r[1]}</b>
                <span>
                    {r[2]}
                </span>
            </div>
            <div>
                {r[3]}
            </div>
            <button
                onclick="deleteRisk('{r[0]}')"
            >
                删除
            </button>
        </div>
        """
    return f"""
    <div class='project-detail-wrap'>
        <h2>{detail[0]}</h2>
        <p>负责人：{detail[1]}</p>
        <p>周期：{detail[2]}</p>
        <p>进度：{detail[3]}</p>
        <p>延期：{detail[4]}</p>
        <p>风险等级：{detail[5]}</p>
        <button
        class="blue-btn"
        onclick="aiProjectReport('{project_id}')"
        style="
            margin-top:10px;
            margin-bottom:20px;
        "
        >
        🤖 AI项目分析
    </button>
        <hr>
        <h3>项目成员</h3>
        <ul>
        {member_html}
        </ul>
        <hr>
           <h3>项目进展记录</h3>
          {progress_html}
        <hr>
            <h3>风险记录</h3>
            {risk_html}
    </div>
    """

#新增成员Service
def add_project_member(
        project_id,
        username,
        real_name,
        role
):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        insert into project_member(
            project_id,
            username,
            real_name,
            role_in_project

        )
        values(?,?,?,?)
        """,
        (
            project_id,
            username,
            real_name,
            role
        )
    )
    conn.commit()
    conn.close()
    return "添加成功"

#刷新详情页
def add_member_and_refresh(
        project_id,
        member_name,
        role
):

    add_project_member(
        project_id,
        member_name,
        role
    )

    return build_project_detail_html(
        project_id
    )

#项目详情统计
def get_project_statistics(project_id):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select count(*)
        from project_member
        where project_id=?
        """,
        (project_id,)
    )

    member_count = cur.fetchone()[0]

    cur.execute(
        """
        select count(*)
        from project_risk
        where project_id=?
        """,
        (project_id,)
    )

    risk_count = cur.fetchone()[0]

    cur.execute(
        """
        select count(*)
        from project_progress
        where project_id=?
        """,
        (project_id,)
    )

    progress_count = cur.fetchone()[0]

    conn.close()

    return {
        "progress_count": progress_count,
        "risk_count": risk_count,
        "member_count": member_count
    }

#删除成员
def delete_project_member(member_id):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        delete from project_member
        where id=?
        """,
        (member_id,)
    )

    conn.commit()

    conn.close()

    return True

#成员统计
def get_member_count(project_id):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select count(*)
        from project_member
        where project_id=?
        """,
        (project_id,)
    )

    count = cur.fetchone()[0]

    conn.close()

    return count

#新增风险
def add_project_risk(
        project_id,
        level,
        content,
        solution
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        insert into project_risk(

            project_id,
            risk_level,
            risk_content,
            solution

        )
        values(?,?,?,?)
        """,
        (
            project_id,
            level,
            content,
            solution
        )
    )

    conn.commit()

    conn.close()

    return True

#删除风险
def delete_project_risk(risk_id):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        delete from project_risk
        where id=?
        """,
        (risk_id,)
    )

    conn.commit()

    conn.close()

    return True

#修改风险
def update_project_risk(
        risk_id,
        level,
        content,
        solution
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        update project_risk

        set

            risk_level=?,
            risk_content=?,
            solution=?

        where id=?
        """,
        (
            level,
            content,
            solution,
            risk_id
        )
    )

    conn.commit()

    conn.close()

    return True

#刷新风险
def add_risk_and_refresh(
        project_id,
        level,
        content,
        solution
):

    add_project_risk(
        project_id,
        level,
        content,
        solution
    )

    return build_project_detail_html(
        project_id
    )

#删除风险和刷新
def delete_risk_and_refresh(
        risk_id,
        project_id
):

    delete_project_risk(risk_id)

    return build_project_detail_html(
        project_id
    )

#项目健康度
def calculate_health_score(project_id):
    stat = get_project_statistics(
        project_id
    )
    score = 100
    score -= stat["risk_count"] * 10
    detail = get_project_detail(
        project_id
    )
    if detail:
        is_delay = detail[4]
        if is_delay == "是":
            score -= 20
    score = max(score, 0)
    return score

#风险指数
def calculate_risk_index(project_id):
    risks = get_project_risks(
        project_id
    )
    risk_score = 0
    for r in risks:
        level = r[0]
        if level == "低":
            risk_score += 1
        elif level == "中":
            risk_score += 3
        elif level == "高":
            risk_score += 5
    return risk_score

#AI分析
def build_project_ai_analysis(
        project_id
):
    detail = get_project_detail(
        project_id
    )

    members = get_project_members(
        project_id
    )

    risks = get_project_risks(
        project_id
    )

    progress = get_project_progress(
        project_id
    )

    health_score = calculate_health_score(
        project_id
    )

    risk_index = calculate_risk_index(
        project_id
    )

    prompt = f"""
    你是资深项目管理顾问。

    请分析项目。

    项目名称:
    {detail[0]}

    负责人:
    {detail[1]}

    项目进度:
    {detail[3]}

    项目成员:
    {members}

    项目风险:
    {risks}

    项目进展:
    {progress}

    健康度:
    {health_score}

    风险指数:
    {risk_index}

    请输出：

    【项目健康度】

    【项目现状】

    【风险分析】

    【延期概率】

    【管理建议】
    """
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

def build_project_progress_html(real_name):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select project_name
        from project
        where main_leader like ?
        limit 5
    """,(f"%{real_name}%",))

    rows = cur.fetchall()

    conn.close()

    html = """
    <div class="dashboard-card">

        <div class="card-title">
            我负责的项目
        </div>

        <table class="project-table">

            <tr>
                <th>项目名称</th>
                <th>状态</th>
            </tr>
    """

    for r in rows:

        html += f"""
        <tr>
            <td>{r[0]}</td>
            <td>进行中</td>
        </tr>
        """

    html += "</table></div>"

    return html

#项目健康度排行榜
def get_project_health_rank():
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute("""
    select
        id,
        project_name
    from project
    """)
    rows = cur.fetchall()
    conn.close()
    result = []
    for row in rows:
        pid = row[0]
        score = calculate_health_score(pid)
        result.append(
            (
                row[1],
                score
            )
        )
    result.sort(
        key=lambda x:x[1],
        reverse=True
    )
    return result

def build_project_health_rank_html():
    rows = get_project_health_rank()
    html = """
    <div class='rank-card'>
    <table class='rank-table'>
        <thead>
            <tr>
                <th>排名</th>
                <th>项目</th>
                <th>健康度</th>
            </tr>
        </thead>
        <tbody>
    """

    for idx,row in enumerate(
            rows,
            start=1
    ):
        html += f"""
        <tr>
            <td>{idx}</td>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
        </tr>
        """
    html += """
        </tbody>
    </table>
    </div>
    """
    return html

#风险预警中心
def get_risk_warning_projects():
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute("""
    select
        id,
        project_name,
        is_delay
    from project
    """)
    projects = cur.fetchall()
    conn.close()
    warnings = []
    for p in projects:
        pid = p[0]
        risk_index = calculate_risk_index(pid)
        health = calculate_health_score(pid)
        if risk_index >= 10:
            warnings.append(
                (
                    p[1],
                    "高风险",
                    risk_index,
                    health
                )
            )

        elif health <= 60:
            warnings.append(
                (
                    p[1],
                    "健康度过低",
                    risk_index,
                    health
                )
            )
    return warnings

def build_risk_warning_html():
    rows = get_risk_warning_projects()
    html = ""
    for row in rows:
        html += f"""
        <div class='warning-card'>
            <div>
                <b>{row[0]}</b>
            </div>
            <div>
                类型：{row[1]}
            </div>
            <div>
                风险指数：{row[2]}
            </div>
            <div>
                健康度：{row[3]}
            </div>
        </div>
        """
    return html

def build_submit_timeline_html(real_name):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select report_date
        from daily_report
        where reporter=?
        order by report_date desc
        limit 5
    """,(real_name,))

    rows = cur.fetchall()

    conn.close()

    html = """
    <div class="dashboard-card">

        <div class="card-title">
            最近提交记录
        </div>

        <div class="timeline">
    """

    for r in rows:

        html += f"""
        <div class="timeline-item">
            📄 日报提交
            <span>{r[0]}</span>
        </div>
        """

    html += "</div></div>"

    return html



