import requests
import re
from datetime import datetime
from common.db import get_project_conn
import json

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

#AI日报
def generate_ai_daily(user):

    return f"""
    <div class='ai-output'>

    <h3>AI日报</h3>

    今日完成：

    1. Dashboard开发

    2. 项目功能优化

    3. AI助手集成

    明日计划：

    1. AI周报

    2. AI项目分析

    </div>
    """


#AI周报
def generate_ai_weekly(user):

    return """
    <div class='ai-output'>

    <h3>AI周报</h3>

    本周完成：

    Dashboard V15

    项目管理

    AI工作助手

    </div>
    """

#AI项目总结
def generate_project_summary(user):

    return """
    <div class='ai-output'>

    <h3>项目总结</h3>

    当前项目：

    华智瑞森特工作流管理系统

    当前状态：

    开发中

    风险：

    无

    </div>
    """

#AI会议记录
def generate_ai_meeting_summary(real_name):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select
            meet_title,
            meet_content,
            task_problem,
        from meeting
        where sponsor=?
        order by id desc
        limit 1
    """,(real_name,))

    row = cur.fetchone()

    conn.close()

    if not row:

        return """
        <div class='ai-output'>

        未找到会议记录

        </div>
        """

    theme = row[0]
    content = row[1]
    result = row[2]

    return f"""
    <div class='ai-output'>

    <h3>📅 AI会议纪要</h3>

    <b>会议主题：</b><br>
    {theme}

    <br><br>

    <b>会议内容总结：</b><br>
    {content}

    <br><br>

    <b>会议结论：</b><br>
    {result}

    <br><br>

    <b>AI提炼：</b><br>

    会议主要围绕：
    {theme}

    展开讨论。

    建议后续形成任务清单并持续跟踪。

    </div>
    """

def calc_level(progress,risk,end_date):

    score = 0

    if progress < 30:
        score += 40

    elif progress < 60:
        score += 20

    if risk and risk != "无":
        score += 40

    try:

        days = (
            datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ) -
            datetime.now()
        ).days

        if days < 7:
            score += 30

        elif days < 15:
            score += 15

    except:
        pass

    if score >= 70:
        return "🔴 高风险"

    elif score >= 40:
        return "🟠 中风险"

    return "🟢 低风险"

def call_ollama(
        prompt,
        model="deepseek-r1:8b"
):

    try:

        resp = requests.post(

            "http://127.0.0.1:11434/api/generate",

            json={

                "model": model,

                "prompt": prompt,

                "stream": False

            },

            timeout=600

        )

        result = resp.json()

        return result.get(
            "response",
            ""
        )

    except Exception as e:

        return str(e)

def generate_ai_risk_report(
        real_name
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select
            project_name,
            main_leader,
            progress,
            risk_block,
            end_date
        from project
        where
            main_leader like ?
            or developers like ?
            or testers like ?
            or designer like ?
            or structure_engineer like ?
    """,
    (
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%"
    ))

    projects = cur.fetchall()

    conn.close()

    project_text = ""

    for p in projects:

        project_text += f"""
            项目名称:{p[0]}
            负责人:{p[1]}
            当前进度:{p[2]}
            风险:{p[3]}
            截止时间:{p[4]}
            ----------------
            """

    prompt = f"""
    你是一名资深项目总监。
    
    请根据以下项目情况生成风险预警报告。
    
    要求输出：
    
    【项目名称】
    
    【风险等级】
    高风险/中风险/低风险
    
    【风险原因】
    
    【影响范围】
    
    【解决建议】
    
    【负责人】
    
    【预计延期天数】
    
    项目数据：
    
    {project_text}
    """

    result = call_ollama(

        prompt,

        model="deepseek-r1:8b"

    )

    return result

#新增知识库搜索
def search_user_knowledge(
        question
):

    conn = get_project_conn()

    cur = conn.cursor()

    result = []

    q = f"%{question}%"

    # 日报

    cur.execute("""
    select
        report_date,
        reporter,
        report_content
    from daily_report
    where report_content like ?
    limit 20
    """,
    (q,)
    )

    for r in cur.fetchall():

        result.append(

            f"""
[日报]

日期:{r[0]}

人员:{r[1]}

内容:

{r[2]}
"""
        )

    # 会议

    cur.execute("""
    select
        meet_date,
        sponsor,
        meet_content
    from meeting
    where meet_content like ?
    limit 20
    """,
    (q,)
    )

    for r in cur.fetchall():

        result.append(

            f"""
[会议]

日期:{r[0]}

主持人:{r[1]}

内容:

{r[2]}
"""
        )

    # 项目

    cur.execute("""
    select
        project_name,
        progress,
        risk_block
    from project
    where
        project_name like ?
        or risk_block like ?
    limit 20
    """,
    (q, q)
    )

    for r in cur.fetchall():

        result.append(

            f"""
[项目]

项目:

{r[0]}

进度:

{r[1]}

风险:

{r[2]}
"""
        )

    conn.close()

    return "\n".join(result)

#新增AI问答主函数
def ai_rag_chat(
        question
):

    knowledge = search_user_knowledge(
        question
    )

    if knowledge:

        prompt = f"""
你是企业AI助手。

优先依据知识库回答。

知识库内容：

{knowledge}

用户问题：

{question}

要求：

1. 优先引用知识库
2. 如果知识库不足可结合常识补充
3. 中文回答
"""

        return call_ollama(
            prompt,
            "deepseek-r1:8b"
        )

    return call_ollama(
        question,
        "deepseek-r1:8b"
    )
