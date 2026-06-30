from common.db import get_project_conn
from datetime import datetime
from common.project_db import (
    get_all_project,
    get_project_owner
)

def create_ai_task(
        project_name,
        title,
        desc,
        assignee,
        priority,
        deadline
):

    conn = get_project_conn()

    cur = conn.cursor()

    assignee = auto_assign_owner(
        project_name
    )

    cur.execute(
        """
        insert into ai_task(
            project_name,
            task_title,
            task_desc,
            assignee,
            priority,
            deadline,
            status,
            create_time
        )
        values(
            ?,?,?,?,?,?,
            '待处理',
            ?
        )
        """,
        (
            project_name,
            title,
            desc,
            assignee,
            priority,
            deadline,
            str(
                datetime.now()
            )
        )
    )
    conn.commit()
    conn.close()

def get_ai_tasks():
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select *

        from ai_task

        order by id desc
        """
    )

    rows = cur.fetchall()
    conn.close()
    return rows

#项目健康评分
def calculate_project_health():

    projects = get_all_project()

    result = []

    for p in projects:

        progress = p.get(
            "progress",
            0
        )

        try:

            progress = int(progress)

        except:

            progress = 0

        score = 100

        if progress < 30:

            score -= 40

        elif progress < 60:

            score -= 20

        result.append({

            "project":
            p["project_name"],

            "progress":
            progress,

            "score":
            score

        })

    return result

#AI识别风险
def detect_project_risk():

    projects = calculate_project_health()

    risk_list = []

    for p in projects:

        if p["score"] < 70:

            risk_list.append({

                "project_name":
                p["project"],

                "score":
                p["score"],

                "risk_text": f"""
                项目：{p['project']}

                当前健康度：{p['score']}

                建议：
                1.检查项目进度
                2.检查负责人反馈
                3.制定整改计划
                """

            })

    return risk_list

#AI自动生成任务
def auto_create_tasks():

    risks = detect_project_risk()

    count = 0

    for risk in risks:

        project_name = risk["project_name"]

        create_ai_task(

            project_name=project_name,

            title="项目风险整改",

            desc=risk["risk_text"],

            assignee=
            auto_assign_owner(
                project_name
            ),

            priority="高",

            deadline="3天内"

        )

        count += 1

    return f"创建任务 {count} 条"

def auto_assign_owner(
        project_name
):
    owner = get_project_owner(
        project_name
    )
    if owner:
        return owner
    return "admin"