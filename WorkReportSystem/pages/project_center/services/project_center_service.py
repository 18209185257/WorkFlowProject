from common.db import get_project_conn
import requests
from common.config import (
    API_HOST,
    TOKEN,
    TODAY
)
from collections import Counter
import os
import json


def get_project_list():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select

        id,
        project_name,
        project_cycle,
        main_leader,
        participants,
        is_delay,
        risk_block,
        progress,
        update_time,

        developers,
        testers,
        designer,
        structure_engineer,

        start_date,
        end_date

    from project

    order by id desc
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def build_project_html():

    rows = get_project_list()

    html = """
    <div class="user-table">

        <div class="user-manage-row header">

            <div>项目名称</div>

            <div>负责人</div>

            <div>周期</div>

            <div>进度</div>

            <div>延期</div>

            <div>风险</div>

            <div>操作</div>

        </div>
    """

    for row in rows:
        pid = row[0]

        project_name = row[1]

        leader = row[3]

        participants = row[4]

        delay = row[5]

        risk = row[6]

        progress = row[7]

        update_time = row[8]

        developers = row[9] or ""
        testers = row[10] or ""
        designer = row[11] or ""
        structure = row[12] or ""
        start_date = row[13] or ""
        end_date = row[14] or ""

        if start_date and end_date:
            project_cycle = f"{start_date} ~ {end_date}"
        else:
            project_cycle = row[2] or ""

        html += f"""
        <div class="user-manage-row">

            <div>{project_name}</div>

            <div>{leader}</div>

            <div>{project_cycle}</div>

            <div>{progress}</div>

            <div>{delay}</div>

            <div>{risk}</div>

            <div>

                <button
                    class="edit-btn"

                    onclick="editProject(
                        '{pid}',
                        `{project_name}`,
                        `{leader}`,
                        `{developers}`,
                        `{testers}`,
                        `{designer}`,
                        `{structure}`,
                        '{start_date}',
                        '{end_date}',
                        `{progress}`,
                        '{delay}',
                        `{risk}`
                    )"
                >
                    编辑
                </button>

                <button
                    class="delete-btn"
                    onclick="deleteProject(
                        '{pid}',
                        `{project_name}`
                    )"
                >
                    删除
                </button>

                <button
                class="edit-btn"
            
                onclick="viewProject(
                    `{project_name}`,
                    `{leader}`,
                    `{developers}`,
                    `{testers}`,
                    `{designer}`,
                    `{structure}`,
                    '{start_date}',
                    '{end_date}',
                    `{progress}`,
                    '{delay}',
                    `{risk}`
                )"
            >
                详情
            </button>

            </div>

        </div>
        """
    html += "</div>"
    return html

def update_project_api(data):

    requests.post(
        f"{API_HOST}/api/update_project",
        data={

            "token": TOKEN,

            "project_id": data["id"],

            "project_name": data["project_name"],

            "main_leader": data["main_leader"],

            "developers": data["developers"],
            "testers": data["testers"],
            "designer": data["designer"],
            "structure_engineer": data["structure"],

            "start_date": data["start_date"],
            "end_date": data["end_date"],

            "progress": data["progress"],

            "is_delay": data["delay"],

            "risk_block": data["risk"]

        }
    )
def delete_project_api(project_id):
    requests.post(
        f"{API_HOST}/api/delete_project",
        data={
            "token":TOKEN,
            "project_id":project_id
        }
    )

def get_project_statistics():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        "select count(*) from project"
    )
    total = cur.fetchone()[0]

    cur.execute(
        "select count(*) from project where is_delay='是'"
    )
    delay = cur.fetchone()[0]

    cur.execute(
        "select count(*) from project where risk_block='高'"
    )
    risk = cur.fetchone()[0]

    cur.execute(
        """
        select count(distinct main_leader)
        from project
        """
    )
    leader_count = cur.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "delay": delay,
        "risk": risk,
        "leader_count": leader_count
    }

def build_project_kpi_html():

    stat = get_project_statistics()

    return f"""
    <div class="project-kpi-wrap">

        <div class="project-kpi-card">
            <div class="kpi-num">{stat['total']}</div>
            <div class="kpi-title">项目总数</div>
        </div>

        <div class="project-kpi-card">
            <div class="kpi-num delay">
                {stat['delay']}
            </div>
            <div class="kpi-title">延期项目</div>
        </div>

        <div class="project-kpi-card">
            <div class="kpi-num risk">
                {stat['risk']}
            </div>
            <div class="kpi-title">风险项目</div>
        </div>

        <div class="project-kpi-card">
            <div class="kpi-num">
                {stat['leader_count']}
            </div>
            <div class="kpi-title">负责人数量</div>
        </div>

    </div>
    """

def build_project_rank_html():

    projects = get_project_list()

    counter = Counter()

    for p in projects:

        leader = p[3]

        if leader:
            counter[leader] += 1

    rows = ""

    for idx, (name, count) in enumerate(
        counter.most_common(10),
        start=1
    ):

        rows += f"""
        <tr>
            <td>{idx}</td>
            <td>{name}</td>
            <td>{count}</td>
        </tr>
        """

    return f"""
    <div class="rank-card">

        <table class="rank-table">

            <thead>
                <tr>
                    <th>排名</th>
                    <th>负责人</th>
                    <th>项目数</th>
                </tr>
            </thead>

            <tbody>
                {rows}
            </tbody>

        </table>

    </div>
    """

#新增项目保存数据库
def add_project(
        project_name,

        start_date,
        end_date,

        leader,

        developers,
        testers,
        designer,
        structure_engineer,

        progress,

        delay,

        risk
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO project(

            project_name,

            start_date,
            end_date,

            main_leader,

            developers,
            testers,
            designer,
            structure_engineer,

            progress,

            is_delay,

            risk_block,

            update_time

        )
        VALUES(
            ?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (

            project_name,

            start_date,
            end_date,

            leader,

            developers,
            testers,
            designer,
            structure_engineer,

            progress,

            delay,

            risk,

            TODAY

        )
    )

    conn.commit()

    conn.close()

    return "新增成功"


#编辑项目保存
def update_project(
        pid,
        project_name,
        leader,
        progress,
        delay,
        risk
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE project
        SET

            project_name=?,
            main_leader=?,
            progress=?,
            is_delay=?,
            risk_block=?

        WHERE id=?
        """,
        (
            project_name,
            leader,
            progress,
            delay,
            risk,
            pid
        )
    )

    conn.commit()

    conn.close()

    return "修改成功"

#删除项目
def delete_project(pid):

    conn = get_project_conn()

    cur = conn.cursor()

    # 删除成员
    cur.execute(
        """
        DELETE FROM project_member
        WHERE project_id=?
        """,
        (pid,)
    )

    # 删除风险
    cur.execute(
        """
        DELETE FROM project_risk
        WHERE project_id=?
        """,
        (pid,)
    )

    # 删除进展
    cur.execute(
        """
        DELETE FROM project_progress
        WHERE project_id=?
        """,
        (pid,)
    )

    # 删除项目
    cur.execute(
        """
        DELETE FROM project
        WHERE id=?
        """,
        (pid,)
    )

    conn.commit()

    conn.close()

def add_project_api(data):

    payload = {
        "token": TOKEN,
        "project_name": data["project_name"],
        "main_leader": data["main_leader"],
        "developers": data["developers"],
        "testers": data["testers"],
        "designer": data["designer"],
        "structure_engineer": data["structure"],
        "start_date": data["start_date"],
        "end_date": data["end_date"],
        "progress": data["progress"],
        "is_delay": data["delay"],
        "risk_block":  data.get("risk","无") or "无",
        "project_cycle": f"{data['start_date']}~{data['end_date']}",
        "participants": (
                data["developers"]
                + "," +
                data["testers"]
        )
    }

    print("发送数据=", payload)

    r = requests.post(
        f"{API_HOST}/api/add_project",
        data=payload
    )

    print("状态码=", r.status_code)
    print("返回内容=", r.text)


