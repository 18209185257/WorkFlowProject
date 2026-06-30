from common.project_db import (
    get_all_project
)

from .ai_task_service import (
    calculate_project_health
)


def build_project_health_html():

    projects = calculate_project_health()

    html = """
    <div class='leader-card'>

        <h3>
        项目健康排行
        </h3>
    """

    projects = sorted(
        projects,
        key=lambda x: x["score"],
        reverse=True
    )

    for p in projects:

        color = "#22c55e"

        if p["score"] < 70:

            color = "#f59e0b"

        if p["score"] < 50:

            color = "#ef4444"

        html += f"""
        <div style="
            padding:10px;
            border-bottom:1px solid #333;
        ">

            {p['project']}

            <span style="
                float:right;
                color:{color};
                font-weight:bold;
            ">

                {p['score']}

            </span>

        </div>
        """

    html += "</div>"

    return html

def build_pm_insight():

    return """
    <div class='leader-card'>

    <h3>

    🤖 AI项目经理洞察

    </h3>

    <ul>

        <li>
        当前高风险项目:
        3个
        </li>

        <li>
        建议重点关注
        项目进度低于50%
        的项目
        </li>

        <li>
        建议本周补充
        风险复盘会议
        </li>

    </ul>

    </div>
    """

