from common.config import TODAY
from common.db import get_project_conn


# ==========================
# 日报总结
# ==========================

def get_daily_summary_html():

    try:

        conn = get_project_conn()
        cur = conn.cursor()

        cur.execute("""
        select count(*)
        from daily_report
        where report_date=?
        """,(TODAY,))

        today_count = cur.fetchone()[0]

        cur.execute("""
        select count(*)
        from daily_report
        """)

        total_count = cur.fetchone()[0]

        conn.close()

        return f"""
        <div class='side-card'>

            <div class='side-title'>
                📝 AI日报总结
            </div>

            <div class='side-body'>

                <p>
                    今日提交日报：
                    <b>{today_count}</b>
                    份
                </p>

                <p>
                    累计日报：
                    <b>{total_count}</b>
                    份
                </p>

                <p>
                    AI建议：
                    今日团队工作状态正常。
                </p>

            </div>

        </div>
        """

    except Exception as e:

        return f"""
        <div class='side-card'>
            日报统计异常：
            {e}
        </div>
        """


# ==========================
# 风险分析
# ==========================

def get_risk_summary_html():
    try:
        conn = get_project_conn()
        cur = conn.cursor()
        cur.execute("""
        select
            p.project_name,
            r.risk_level

        from project_risk r

        left join project p
        on r.project_id = p.id

        order by r.id desc
        limit 5
        """)

        rows = cur.fetchall()

        conn.close()

        if not rows:

            return """
            <div class='side-card'>

                <div class='side-title'>
                    ⚠ AI风险分析
                </div>

                <div class='side-body'>
                    暂无风险记录
                </div>

            </div>
            """

        html = ""

        for row in rows:

            html += f"""
            <div class='risk-row'>

                <span>
                    {row[0]}
                </span>

                <span class='risk-tag'>
                    {row[1]}
                </span>

            </div>
            """

        return f"""
        <div class='side-card'>

            <div class='side-title'>
                ⚠ AI风险分析
            </div>

            <div class='side-body'>

                {html}

            </div>

        </div>
        """

    except Exception as e:

        return f"""
        <div class='side-card'>
            风险统计异常：
            {e}
        </div>
        """


# ==========================
# 项目排行榜
# ==========================

def get_project_rank_html():

    try:

        conn = get_project_conn()
        cur = conn.cursor()

        cur.execute("""
        select
            project_name,
            progress
        from project
        order by progress desc
        limit 5
        """)

        rows = cur.fetchall()

        conn.close()

        if not rows:

            return """
            <div class='side-card'>

                <div class='side-title'>
                    📈 项目进度排行榜
                </div>

                <div class='side-body'>
                    暂无项目
                </div>

            </div>
            """

        html = ""

        rank = 1

        for row in rows:

            progress = row[1] or 0

            html += f"""
            <div class='rank-row'>

                <span>
                    TOP{rank}
                </span>

                <span>
                    {row[0]}
                </span>

                <span>
                    {progress}%
                </span>

            </div>
            """

            rank += 1

        return f"""
        <div class='side-card'>

            <div class='side-title'>
                📈 项目进度排行榜
            </div>

            <div class='side-body'>

                {html}

            </div>

        </div>
        """

    except Exception as e:

        return f"""
        <div class='side-card'>
            排行榜异常：
            {e}
        </div>
        """


# ==========================
# KPI统计
# ==========================

def get_ai_dashboard_kpi():

    try:

        conn = get_project_conn()
        cur = conn.cursor()

        cur.execute(
            "select count(*) from project"
        )

        project_count = cur.fetchone()[0]

        cur.execute("""
        select count(*)
        from project_risk
        """)

        risk_count = cur.fetchone()[0]

        cur.execute("""
        select count(*)
        from project_progress
        """)

        progress_count = cur.fetchone()[0]

        conn.close()

        return (
            project_count,
            progress_count,
            risk_count
        )

    except:

        return (
            0,
            0,
            0
        )


# ==========================
# KPI卡片
# ==========================

def build_kpi_html():

    project_count,progress_count,risk_count = (
        get_ai_dashboard_kpi()
    )

    return (

        f"""
        <div class='kpi-card'>
            <span>项目总数</span>
            <h2>{project_count}</h2>
        </div>
        """,

        f"""
        <div class='kpi-card'>
            <span>项目进展</span>
            <h2>{progress_count}</h2>
        </div>
        """,

        f"""
        <div class='kpi-card'>
            <span>风险项目</span>
            <h2>{risk_count}</h2>
        </div>
        """
    )


# ==========================
# AI侧边栏
# ==========================

def build_ai_side_panel():

    summary_html = (
        get_daily_summary_html()
    )

    risk_html = (
        get_risk_summary_html()
    )

    rank_html = (
        get_project_rank_html()
    )

    return (
        summary_html,
        risk_html,
        rank_html
    )
