import sqlite3
from datetime import datetime
import requests
from fastapi import FastAPI, Query, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import re
import json
# 启动 main.py
from common.config import (
    DB_PATH,
    DB_USER_PATH
)
# 启动 db.py
# from config import (
#     DB_PATH,
#     DB_USER_PATH
# )

print(DB_PATH)

# ===================== 全局配置 =====================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"
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
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA cache_size=-8000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA temp_store=MEMORY;")
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS project (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_name TEXT,
    
        start_date TEXT,
        end_date TEXT,
    
        main_leader TEXT,
    
        developers TEXT,
        testers TEXT,
        designer TEXT,
        structure_engineer TEXT,
    
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

    cur.execute('''
    CREATE TABLE IF NOT EXISTS project_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        progress_date TEXT,
        progress_content TEXT,
        risk_content TEXT,
        next_plan TEXT,
        reporter TEXT,
        create_time TEXT
    )
    ''')

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_follow (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        contact_person TEXT,
        contact_phone TEXT,
        sales_name TEXT,
        customer_level TEXT,
        customer_status TEXT,
        follow_stage TEXT,
        follow_content TEXT,
        next_action TEXT,
        next_follow_date TEXT,
        create_time TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales_order (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        customer_name TEXT,

        project_name TEXT,

        sales_name TEXT,

        order_amount REAL,

        order_status TEXT,

        sign_date TEXT,

        expected_delivery_date TEXT,

        actual_delivery_date TEXT,

        create_time TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payment_record (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        customer_name TEXT,

        order_id INTEGER,

        sales_name TEXT,

        payment_amount REAL,

        payment_date TEXT,

        payment_type TEXT,

        remark TEXT,

        create_time TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS project_detail(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        project_desc TEXT,

        project_goal TEXT,

        start_date TEXT,

        end_date TEXT,

        budget REAL,

        create_time TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS project_member(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        username TEXT,

        real_name TEXT,
        
        member_name TEXT,

        role_in_project TEXT,

        create_time TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS project_risk(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        risk_level TEXT,

        risk_content TEXT,

        solution TEXT,

        create_user TEXT,

        create_time TEXT
    )
    """)

    #AI任务追踪表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS task_tracker (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    source_type TEXT,

    source_id INTEGER,

    owner TEXT,

    task_content TEXT,

    deadline TEXT,

    status TEXT,

    create_time TEXT
    )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS customer(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
    
        customer_name TEXT,
    
        contact_name TEXT,
    
        phone TEXT,
    
        email TEXT,
    
        address TEXT,
    
        create_time TEXT
    )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS project_risk_ai (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
    
        project_id INTEGER,
    
        risk_level TEXT,
    
        risk_score INTEGER,
    
        ai_result TEXT,
    
        create_time TEXT

    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS notification (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        receiver TEXT,

        title TEXT,

        content TEXT,

        is_read INTEGER DEFAULT 0,

        create_time TEXT

    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ai_conversation(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        role TEXT,
        content TEXT,
        create_time TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ai_memory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        memory_type TEXT,
        memory_content TEXT,
        score REAL DEFAULT 1.0,
        create_time TEXT
    )
    """)

    conn.commit()
    conn.close()

def upgrade_project_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(project)")
    cols = [x[1] for x in cur.fetchall()]

    add_columns = {
        "developers":"TEXT",
        "testers":"TEXT",
        "designer":"TEXT",
        "structure_engineer":"TEXT",
        "start_date":"TEXT",
        "end_date":"TEXT"
    }

    for col,col_type in add_columns.items():

        if col not in cols:

            cur.execute(
                f"ALTER TABLE project "
                f"ADD COLUMN {col} {col_type}"
            )

    conn.commit()
    conn.close()

def get_project_conn():
    return sqlite3.connect(DB_PATH)

def get_conn():
    return sqlite3.connect(DB_USER_PATH)

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
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(sql, params)
    res = cur.fetchall()
    conn.close()
    return res

# 通用插入
def db_insert(sql: str, params: tuple):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    conn.close()

def user_db_query(
        sql: str,
        params: tuple = ()
):

    conn = sqlite3.connect(DB_USER_PATH)

    cur = conn.cursor()

    cur.execute(sql, params)

    res = cur.fetchall()

    conn.close()

    return res

# 统一鉴权
def check_token(token: str):
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="密钥错误")

init_db()
upgrade_project_table()

# ==========新增提交接口不变==========
@app.post("/api/add_project")
def add_project(
    token: str = Form(...),
    project_name: str = Form(...),
    main_leader: str = Form(...),
    developers: str = Form(""),
    testers: str = Form(""),
    designer: str = Form(""),
    structure_engineer: str = Form(""),
    start_date: str = Form(""),
    end_date: str = Form(""),
    progress: str = Form(""),
    is_delay: str = Form("否"),
    risk_block: str = Form("")
):
    print("进入add_project")

    check_token(token)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    insert into project(

        project_name,

        main_leader,

        developers,
        testers,
        designer,
        structure_engineer,

        start_date,
        end_date,

        progress,

        is_delay,

        risk_block,

        update_time

    )
    values(
        ?,?,?,?,?,?,?,?,?,?,?,?
    )
    """,
                (
                    project_name,

                    main_leader,

                    developers,
                    testers,
                    designer,
                    structure_engineer,

                    start_date,
                    end_date,

                    progress,

                    is_delay,

                    risk_block,
                    datetime.now().strftime("%Y-%m-%d")
                ))
    conn.commit()
    conn.close()
    return {"code":200}

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

    conn = sqlite3.connect(DB_PATH)
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

# 查询用户列表
@app.get("/api/user_list")
def get_user_list(token: str = Query(...)):
    check_token(token)
    sql = """
    SELECT
        username,
        role,
        real_name,
        phone,
        create_time
    FROM users
    ORDER BY id DESC
    """
    data = user_db_query(sql)
    return {
        "code": 200,
        "data": data
    }
# 新增客户
@app.post("/api/add_customer")
def add_customer(
    token: str = Form(...),
    customer_name: str = Form(...),
    contact_person: str = Form(...),
    contact_phone: str = Form(...),
    sales_name: str = Form(...),
    follow_stage: str = Form(...),
    follow_content: str = Form(...),
    next_action: str = Form(...),
    next_follow_date: str = Form(...)
):

    check_token(token)
    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    sql = """
    INSERT INTO customer_follow(
        customer_name,
        contact_person,
        contact_phone,
        sales_name,
        follow_stage,
        follow_content,
        next_action,
        next_follow_date,
        create_time
    )
    VALUES(?,?,?,?,?,?,?,?,?)
    """
    db_insert(
        sql,
        (
            customer_name,
            contact_person,
            contact_phone,

            sales_name,

            follow_stage,
            follow_content,

            next_action,
            next_follow_date,
            now
        )
    )
    return {
        "code":200,
        "msg":"客户新增成功"
    }

#查询客户
@app.get("/api/query_customer")
def query_customer(

    token:str=Query(...),

    customer_name:str="",

    sales_name:str=""
):
    check_token(token)
    sql = """
    SELECT *
    FROM customer_follow
    WHERE 1=1
    """
    params=[]
    if customer_name:

        sql += """
        AND customer_name LIKE ?
        """
        params.append(
            f"%{customer_name}%"
        )
    if sales_name:
        sql += """
        AND sales_name LIKE ?
        """
        params.append(
            f"%{sales_name}%"
        )
    data = db_query(
        sql,
        tuple(params)
    )
    return {
        "code":200,
        "data":data
    }

# 修改客户
@app.post("/api/update_customer")
def update_customer(

    token:str=Form(...),

    customer_id:int=Form(...),

    contact_person:str=Form(...),

    contact_phone:str=Form(...),

    follow_stage:str=Form(...),

    follow_content:str=Form(...),

    next_action:str=Form(...),

    next_follow_date:str=Form(...)
):

    check_token(token)

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("""

    UPDATE customer_follow

    SET

        contact_person=?,
        contact_phone=?,

        follow_stage=?,
        follow_content=?,

        next_action=?,
        next_follow_date=?

    WHERE id=?

    """,(

        contact_person,
        contact_phone,

        follow_stage,
        follow_content,

        next_action,
        next_follow_date,

        customer_id

    ))

    conn.commit()
    conn.close()

    return {
        "code":200,
        "msg":"修改成功"
    }

# 删除客户
@app.post("/api/delete_customer")
def delete_customer(

    token:str=Form(...),

    customer_id:int=Form(...)
):

    check_token(token)

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(

        """
        DELETE FROM customer_follow
        WHERE id=?
        """,

        (customer_id,)
    )

    conn.commit()
    conn.close()

    return {
        "code":200,
        "msg":"删除成功"
    }

@app.post("/api/add_project_center")
def add_project_center(

    token:str=Form(...),

    project_name:str=Form(...),

    project_cycle:str=Form(...),

    main_leader:str=Form(...),

    participants:str=Form(...),

    is_delay:str=Form(...),

    risk_block:str=Form(...),

    progress:str=Form(...)
):

    check_token(token)

    now=datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    conn=sqlite3.connect(DB_PATH)

    cur=conn.cursor()

    cur.execute("""

    insert into project(

        project_name,
        project_cycle,
        main_leader,
        participants,
        is_delay,
        risk_block,
        progress,
        update_time

    )

    values(

        ?,?,?,?,?,?,?,?
    )

    """,(

        project_name,
        project_cycle,
        main_leader,
        participants,
        is_delay,
        risk_block,
        progress,
        now
    ))

    conn.commit()

    conn.close()

    return {
        "code":200
    }

@app.post("/api/update_project")
def update_project(

    token:str=Form(...),

    project_id:int=Form(...),

    project_name:str=Form(...),

    main_leader:str=Form(...),

    developers:str=Form(""),

    testers:str=Form(""),

    designer:str=Form(""),

    structure_engineer:str=Form(""),

    start_date:str=Form(""),

    end_date:str=Form(""),

    progress:str=Form(...),

    is_delay:str=Form(...),

    risk_block:str=Form(...)
):

    check_token(token)

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("""

    update project

    set

        project_name=?,

        main_leader=?,

        developers=?,

        testers=?,

        designer=?,

        structure_engineer=?,

        start_date=?,

        end_date=?,

        progress=?,

        is_delay=?,

        risk_block=?

    where id=?

    """, (

        project_name,

        main_leader,

        developers,

        testers,

        designer,

        structure_engineer,

        start_date,

        end_date,

        progress,

        is_delay,

        risk_block,

        project_id
    ))

    conn.commit()

    conn.close()

    return {
        "code":200
    }

@app.post("/api/delete_project")
def delete_project(

    token:str=Form(...),

    project_id:int=Form(...)
):

    check_token(token)

    conn=sqlite3.connect(DB_PATH)

    cur=conn.cursor()

    cur.execute(

        "delete from project where id=?",

        (project_id,)
    )

    conn.commit()

    conn.close()

    return {
        "code":200
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)