import sqlite3
from datetime import datetime
import requests
from fastapi import FastAPI, Query, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import re
import json

# ===================== 全局配置 =====================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"
DB_FILE = "work_data.db"
API_TOKEN = "WorkFlow2026"
BASE_URL = "http://127.0.0.1:8000/api"
# ====================================================

app = FastAPI(title="新版工作流接口")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据表
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA cache_size=-8000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA temp_store=MEMORY;")
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS project (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        project_cycle TEXT,
        main_leader TEXT,
        participants TEXT,
        is_delay TEXT,
        risk_block TEXT,
        progress TEXT,
        update_time TEXT
    )''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS meeting (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meet_title TEXT,
        sponsor TEXT,
        attendees TEXT,
        meet_date TEXT,
        meet_content TEXT,
        task_problem TEXT,
        create_time TEXT
    )''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS daily_report (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reporter TEXT,
        report_content TEXT,
        report_date TEXT,
        help_item TEXT
    )''')

    conn.commit()
    conn.close()

# 调用大模型
def llm_call(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.2,
        "num_ctx": 8192
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=30)
        return resp.json()["response"]
    except Exception as e:
        return f"模型调用失败：{str(e)}"

# 通用查库
def db_query(sql: str, params: tuple = ()) -> list:
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(sql, params)
    res = cur.fetchall()
    conn.close()
    return res

# 通用插入
def db_insert(sql: str, params: tuple):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    conn.close()

# 统一鉴权
def check_token(token: str):
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="密钥错误")

init_db()

# ==========新增提交接口不变==========
# @app.post("/api/add_project")
# def add_project(
#     token: str = Form(...),
#     project_name: str = Form(...),
#     # project_cycle: str = Form(...),
#     main_leader: str = Form(...),
#     participants: str = Form(...),
#     is_delay: str = Form(...),
#     # risk_block: str = Form(...),
#     progress: str = Form(...)
# ):
#     print("进入add_project")
#     check_token(token)
#     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     sql = '''INSERT INTO project(project_name,project_cycle,main_leader,participants,is_delay,risk_block,progress,update_time)VALUES (?,?,?,?,?,?,?,?)'''
#     db_insert(sql, (project_name, main_leader, participants, is_delay,  progress, now))
#     return {"code": 200, "msg": "项目汇报提交成功"}

@app.post("/api/add_meeting")
def add_meeting(
    token: str = Form(...),
    meet_title: str = Form(...),
    sponsor: str = Form(...),
    attendees: str = Form(...),
    meet_date: str = Form(...),
    meet_content: str = Form(...),
    task_problem: str = Form(...)
):
    check_token(token)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = '''INSERT INTO meeting(meet_title,sponsor,attendees,meet_date,meet_content,task_problem,create_time)VALUES (?,?,?,?,?,?,?)'''
    db_insert(sql, (meet_title, sponsor, attendees, meet_date, meet_content, task_problem, now))
    return {"code": 200, "msg": "会议记录提交成功"}

@app.post("/api/add_report")
def add_report(
    token: str = Form(...),
    reporter: str = Form(...),
    report_content: str = Form(...),
    help_item: str = Form(...),
    report_date: str = Form(None)
):
    check_token(token)
    if report_date and report_date.strip():
        save_date = report_date.strip()
    else:
        save_date = datetime.now().strftime("%Y-%m-%d")
    sql = '''INSERT INTO daily_report(reporter,report_content,report_date,help_item)VALUES (?,?,?,?)'''
    db_insert(sql, (reporter, report_content, save_date, help_item))
    return {"code": 200, "msg": "日报提交成功"}

# 当日汇总
@app.get("/api/today_summary")
def get_today_summary(token: str = Query(...)):
    check_token(token)
    today = datetime.now().strftime("%Y-%m-%d")
    project_list = db_query("SELECT * FROM project WHERE update_time LIKE ?", (f"{today}%",))
    meeting_list = db_query("SELECT * FROM meeting WHERE create_time LIKE ?", (f"{today}%",))
    report_list = db_query("SELECT * FROM daily_report WHERE date(report_date) = date(?)", (today,))

    raw_text = f"【{today} 工作总览】\n==== 项目管理 ====\n"
    for p in project_list:
        raw_text += f"项目名称：{p[1]}，周期：{p[2]}，主负责人：{p[3]}，参与人：{p[4]}，是否延期：{p[5]}，阻碍/风险：{p[6]}，进度：{p[7]}\n"
    raw_text += "\n==== 会议记录 ====\n"
    for m in meeting_list:
        raw_text += f"主题：{m[1]}，发起人：{m[2]}，参会人：{m[3]}，会议日期：{m[4]}，纪要：{m[5]}，Task进展/问题：{m[6]}\n"
    raw_text += "\n==== 员工日报 ====\n"
    for r in report_list:
        raw_text += f"汇报人：{r[1]}，内容：{r[2]}，汇报日期：{r[3]}，求助项：{r[4]}\n"

    prompt = """整理正式精简领导简报，加粗延期、风险、求助，只输出结果，无多余文字：""" + raw_text
    summary = llm_call(prompt)
    return {"code": 200, "data": summary}

# ==========核心：自然查询【支持：朱金涛5月30号会议 /5月30朱金涛会议/5月30会议】==========
@app.get("/api/chat_query")
def chat_query(q: str, token: str = Query(...)):
    check_token(token)
    parse_prompt = '''只输出标准JSON，无任何多余字符。
规则：
1.含会议：type="meet"，date=YYYY-MM-DD，有人名则name=姓名，无则空字符串；
2.含日报：type="report"，name=汇报人名，date=日期；
输出固定格式{"type":"meet|report","date":"","name":""}
用户问题：''' + q
    res_raw = llm_call(parse_prompt).strip()
    try:
        js_start = res_raw.find("{")
        js_end = res_raw.rfind("}") + 1
        json_data = json.loads(res_raw[js_start:js_end])
    except:
        # 解析失败全库兜底
        all_p = db_query("select * from project")
        all_m = db_query("select * from meeting")
        all_r = db_query("select * from daily_report")
        ctx = f"今日{datetime.now().strftime('%Y-%m-%d')}，项目:{all_p},会议:{all_m},日报:{all_r}，无数据回复暂无记录。问题：{q}"
        return {"code": 200, "answer": llm_call(ctx)}

    # 拼接查询链接
    if json_data["type"] == "meet":
        req_url = f'{BASE_URL}/getMeetByDate?token={API_TOKEN}&meet_date={json_data["date"]}'
        if json_data["name"].strip():
            req_url += f'&name={json_data["name"].strip()}'
    elif json_data["type"] == "report":
        req_url = f'{BASE_URL}/query_report?token={API_TOKEN}&user={json_data["name"]}&date={json_data["date"]}'
    else:
        all_p = db_query("select * from project")
        all_m = db_query("select * from meeting")
        all_r = db_query("select * from daily_report")
        ctx = f"项目:{all_p},会议:{all_m},日报:{all_r}，据实回答。问题：{q}"
        return {"code":200,"answer":llm_call(ctx)}

    # 请求查询
    try:
        resp = requests.get(req_url, timeout=8)
        res_json = resp.json()
    except Exception as e:
        return {"code":200,"answer":f"查询异常：{str(e)}"}

    # 结果整理
    fmt_p = f"根据数据精简回答用户提问，无数据直接写暂无相关记录；提问：{q}；查询数据：{res_json}"
    final_ans = llm_call(fmt_p)
    return {"code":200,"answer":final_ans}

# 项目查询
@app.get("/api/query_project")
def query_project(token: str = Query(...), name: str = "", week: str = ""):
    check_token(token)
    sql = "SELECT * FROM project WHERE 1=1"
    param = []
    if name:
        sql += " AND project_name LIKE ?"
        param.append(f"%{name}%")
    if week == "now":
        sql += " AND strftime('%Y',update_time)=strftime('%Y','now') AND strftime('%W',update_time)=strftime('%W','now')"
    return {"code":200,"data":db_query(sql,tuple(param))}

# 全量会议查询
@app.get("/api/query_meeting")
def query_meeting(token: str = Query(...), week: str = ""):
    check_token(token)
    sql = "SELECT * FROM meeting WHERE 1=1"
    param = []
    if week == "now":
        sql += " AND strftime('%Y',meet_date)=strftime('%Y','now') AND strftime('%W',meet_date)=strftime('%W','now')"
    return {"code":200,"data":db_query(sql,tuple(param))}

# 【重点：日期+姓名双筛选会议接口】
@app.get("/api/getMeetByDate")
def get_meet_by_date(token: str, meet_date: str, name: str = ""):
    if token != API_TOKEN:
        return {"code":403,"msg":"token校验失败"}
    cur_year = datetime.now().year
    reg_date = re.compile(r"(\d{1,2})[月\.\-](\d{1,2})")
    match_res = reg_date.search(meet_date)
    if match_res:
        m,d = match_res.groups()
        meet_date = f"{cur_year}-{int(m):02d}-{int(d):02d}"

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    sql = "SELECT * FROM meeting WHERE meet_date LIKE ?"
    args = [f"{meet_date}%"]
    # 姓名：发起人OR参会人包含名字
    if name.strip():
        sql += " AND (sponsor LIKE ? OR attendees LIKE ?)"
        args.extend([f"%{name}%",f"%{name}%"])
    cur.execute(sql,tuple(args))
    data = cur.fetchall()
    conn.close()
    if not data:
        return {"code":200,"data":[],"msg":"未找到当日会议记录"}
    return {"code":200,"data":data}

# 日报查询
@app.get("/api/query_report")
def query_report(token: str = Query(...), user: str = "", date: str = "", week: str = ""):
    check_token(token)
    sql = "SELECT * FROM daily_report WHERE 1=1"
    param = []
    if user:
        sql += " AND reporter LIKE ?"
        param.append(f"%{user}%")
    if date:
        sql += " AND date(report_date)=date(?)"
        param.append(date)
    if week == "now":
        sql += " AND strftime('%Y',report_date)=strftime('%Y','now') AND strftime('%W',report_date)=strftime('%W','now')"
    return {"code":200,"data":db_query(sql,tuple(param))}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)