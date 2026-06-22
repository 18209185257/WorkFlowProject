import requests
import re
from datetime import datetime
from common.db import get_project_conn

# =========================
# Ollama 配置
# =========================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"   # 可换 llama3 / qwen / mistral


# =========================
# 基础AI调用
# =========================
def ask_ai(prompt: str) -> str:
    """
    通用AI调用函数（Ollama）
    """

    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        return res.json().get("response", "")

    except Exception as e:
        return f"AI调用失败：{str(e)}"


# =========================
# Dashboard AI分析
# =========================
import requests

def ai_dashboard_analysis(real_name, kpi_data):

    prompt = f"""
你是企业数据分析AI，请分析该员工数据：

员工：{real_name}

日报：{kpi_data['report']}
会议：{kpi_data['meeting']}
项目：{kpi_data['project']}

请输出：
1. 工作效率评价
2. 风险提示
3. 改进建议
控制在150字以内
"""

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )

        return res.json().get("response", "暂无AI分析")

    except:

        return "AI服务未启动"


# =========================
# 项目风险预测AI
# =========================
def ai_project_risk(project):
    """
    项目风险分析
    """

    prompt = f"""
你是项目风险评估专家：

项目：{project.get('project_name')}
进度：{project.get('progress')}%
是否延期：{project.get('delay')}
风险描述：{project.get('risk')}

请判断：
- 风险等级（高/中/低）
- 主要原因
- 改进建议
"""

    return ask_ai(prompt)


# =========================
# 周报AI生成
# =========================
def ai_weekly_report(reports, meetings, projects):
    """
    自动生成周报
    """

    prompt = f"""
        请根据以下数据生成员工周报：
        
        日报：
        {reports}
        
        会议：
        {meetings}
        
        项目：
        {projects}
        
        输出结构：
        1. 本周完成工作
        2. 问题总结
        3. 下周计划
        """

    return ask_ai(prompt)

def predict_project_risk(project):

    prompt = f"""
        你是一名企业项目风险专家。
        
        项目信息：
        
        项目名称：
        {project['project_name']}
        
        当前进度：
        {project['progress']}
        
        是否延期：
        {project['delay']}
        
        风险说明：
        {project['risk']}
        
        请输出：
        
        风险等级：
        高风险/中风险/低风险
        
        风险评分：
        0~100
        
        风险原因：
        
        解决建议：
        
        输出格式：
        
        风险等级：
        风险评分：
        风险原因：
        解决建议：
        """

    return ask_ai(prompt)

def parse_risk_result(text):
    level = "低风险"
    score = 20

    m = re.search(
        r"风险等级[:：]\s*(.*)",
        text
    )

    if m:
        level = m.group(1).strip()

    m = re.search(
        r"风险评分[:：]\s*(\d+)",
        text
    )

    if m:
        score = int(m.group(1))

    return level, score

def save_project_risk_result(
        project_id,
        level,
        score,
        ai_result
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    insert into project_risk_ai(

        project_id,

        risk_level,

        risk_score,

        ai_result,

        create_time

    )

    values(

        ?,?,?,?,?

    )
    """,(
        project_id,
        level,
        score,
        ai_result,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    conn.commit()

    conn.close()

def run_project_risk_scan():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select

        id,
        project_name,
        progress,
        is_delay,
        risk_block

    from project
    """)

    rows = cur.fetchall()

    conn.close()

    count = 0

    for row in rows:

        project = {

            "project_name": row[1],

            "progress": row[2],

            "delay": row[3],

            "risk": row[4]

        }

        result = predict_project_risk(
            project
        )

        level, score = parse_risk_result(
            result
        )

        save_project_risk_result(
            row[0],
            level,
            score,
            result
        )

        count += 1

    return f"完成扫描 {count} 个项目"

def build_project_risk_rank_html():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select

        p.project_name,

        r.risk_level,

        r.risk_score

    from project_risk_ai r

    left join project p

    on p.id=r.project_id

    order by r.risk_score desc

    limit 10
    """)

    rows = cur.fetchall()

    conn.close()

    html = """
    <div class='risk-panel'>

    <div class='panel-title'>
    🚨 项目风险排行
    </div>
    """

    for row in rows:

        html += f"""
        <div class='risk-row'>

            <span>
            {row[0]}
            </span>

            <span>
            {row[1]}
            </span>

            <span>
            {row[2]}
            分
            </span>

        </div>
        """

    html += "</div>"

    return html

def ai_generate_weekly_report(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    # 日报
    cur.execute("""
        select report_content, report_date
        from daily_report
        where reporter=?
        order by id desc
        limit 20
    """, (real_name,))
    reports = cur.fetchall()

    # 会议
    cur.execute("""
        select meet_title, meet_content, meet_date
        from meeting
        where sponsor=?
        order by id desc
        limit 10
    """, (real_name,))
    meetings = cur.fetchall()

    # 项目
    cur.execute("""
        select project_name, progress, is_delay, risk_block
        from project
        where main_leader like ?
           or developers like ?
           or testers like ?
           or designer like ?
           or structure_engineer like ?
    """, (f"%{real_name}%",)*5)
    projects = cur.fetchall()

    conn.close()

    prompt = f"""
        你是企业AI助手，请根据以下数据生成一份专业周报：
        
        === 日报 ===
        {reports}
        
        === 会议记录 ===
        {meetings}
        
        === 项目情况 ===
        {projects}
        
        请输出：
        
        📌 一、本周完成工作
        📌 二、参与项目情况
        📌 三、会议总结
        📌 四、问题与风险
        📌 五、AI评价（重点）
        📌 六、下周建议
        
        要求：
        - 企业风格
        - 简洁清晰
        - 不超过300字
        """

    return ask_ai(prompt)

