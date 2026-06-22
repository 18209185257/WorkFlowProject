import gradio as gr
import requests
import re
import json
import time
import hashlib
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

API_HOST = "http://127.0.0.1:8000"
TOKEN = "WorkFlow2026"
today_str = datetime.now().strftime("%Y-%m-%d")
curr_year = datetime.now().year

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
LLM_MODEL_NAME = "deepseek-r1:8b"
OLLAMA_TIMEOUT = 40

BUSINESS_KEYWORDS = [
    "项目", "进度", "项目进展", "进展", "日报", "工作总结", "工作汇报", "汇报",
    "工作内容", "明日计划", "会议", "参会", "会议记录", "例会", "工作", "总结", "工作计划"
]

def check_ollama_online():
    try:
        res = requests.get("http://127.0.0.1:11434/api/tags", timeout=3)
        return res.status_code == 200
    except Exception:
        return False


USE_LLM = check_ollama_online()


def deduplicate_data(data_list):
    unique = []
    seen = set()
    if not isinstance(data_list, list):
        return []
    for item in data_list:
        if not isinstance(item, list) or len(item) < 5:
            continue
        content_text = item[2].strip()
        content_hash = hashlib.md5(content_text.encode("utf-8")).hexdigest()
        key = f"{item[3]}|{content_hash}"
        if key not in seen:
            seen.add(key)
            unique.append(item)
    unique.sort(key=lambda x: x[3])
    return unique


def is_business_query(text):
    for kw in BUSINESS_KEYWORDS:
        if kw in text:
            return True
    if re.search(r"\d{1,2}[月号日].*(总结|日报|工作|汇报)", text):
        return True
    if re.search(r"[\u4e00-\u9fa5]{2,}.*(总结|日报|汇报)", text):
        return True
    return False


def normal_ai_answer_stream(question):
    if not USE_LLM:
        yield "【AI离线】"
        return
    prompt = f"""
你是工作数据查询助手，仅简洁回答用户普通问题。
用户问题：{question}
要求：简洁精准回答。
"""
    answer = ""
    try:
        for chunk in ollama_stream(prompt, temperature=0.3, num_ctx=512):
            answer += chunk
            yield answer
    except Exception:
        yield "回答失败"


def regex_parse_query(text):
    single_proj_pat = r"([\u4e00-\u9fa5]+)(项目进度|项目进展|进展|进度)"
    single_proj_match = re.search(single_proj_pat, text)
    if single_proj_match:
        proj_name = single_proj_match.group(1).strip()
        url = f"{API_HOST}/api/query_project?token={TOKEN}&name={proj_name}"
        try:
            res = requests.get(url, timeout=5)
            js = res.json()
            data_list = js.get("data", [])
        except Exception:
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "project", "force_report": False}
        if not data_list:
            raw_text = f"未找到【{proj_name}】相关项目"
        else:
            raw_text = f"===【{proj_name}】项目详情===\n"
            for item in data_list:
                raw_text += f"项目：{item[1]}｜周期：{item[2]}｜负责人：{item[3]}｜延期：{item[5]}｜风险：{item[6]}｜进度：{item[7]}｜更新：{item[8]}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "project", "force_report": False}

    if "本周项目进度" in text or "本周项目进展" in text or "本周进展" in text:
        url = f"{API_HOST}/api/query_project?token={TOKEN}&week=now"
        try:
            js = requests.get(url, timeout=5).json()
            data_list = js.get("data", [])
        except Exception:
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "project", "force_report": False}
        if not data_list:
            raw_text = "本周暂无更新项目"
        else:
            raw_text = "===本周更新项目清单===\n"
            for item in data_list:
                raw_text += f"项目：{item[1]}｜负责人：{item[3]}｜进度：{item[7]}｜延期：{item[5]}｜风险：{item[6]}｜更新时间：{item[8]}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "project", "force_report": False}

    if "项目进度" in text or "项目进展" in text or "进展" in text:
        url = f"{API_HOST}/api/query_project?token={TOKEN}"
        try:
            js = requests.get(url, timeout=5).json()
            data_list = js.get("data", [])
        except Exception:
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "project", "force_report": False}
        if not data_list:
            raw_text = "暂无项目记录"
        else:
            raw_text = "===全部项目清单===\n"
            for item in data_list:
                raw_text += f"项目：{item[1]}｜负责人：{item[3]}｜进度：{item[7]}｜延期：{item[5]}｜风险：{item[6]}｜更新时间：{item[8]}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "project", "force_report": False}

    force_report_flag = True if re.search(r"工作计划|日报|汇报", text) else False
    week_user_pat = r"([\u4e00-\u9fa5]+)本周(工作总结|工作汇报|工作日报)"
    week_user_match = re.search(week_user_pat, text)
    if week_user_match:
        uname = week_user_match.group(1).strip()
        url = f"{API_HOST}/api/query_report?token={TOKEN}&user={uname}&week=now"
        try:
            js = requests.get(url, timeout=5).json()
            raw_all = js.get("data", [])
        except Exception:
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "report", "force_report": force_report_flag}
        data_list = deduplicate_data(raw_all)
        if not data_list:
            raw_text = f"未查到【{uname}】本周日报记录"
        else:
            raw_text = f"========【{uname} 本周全部工作总结】========\n"
            for row in data_list:
                r_date = row[3]
                r_content = row[2]
                r_help = row[4]
                raw_text += f"\n【{r_date}】\n工作内容：{r_content}\n需要协助：{r_help}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "report", "force_report": force_report_flag}

    day_pat = r"([\u4e00-\u9fa5]+)今日工作总结|今日工作汇报"
    day_match = re.search(day_pat, text)
    if day_match:
        uname = day_match.group(1).strip()
        url = f"{API_HOST}/api/query_report?token={TOKEN}&user={uname}&date={today_str}"
        try:
            js = requests.get(url, timeout=5).json()
            raw_all = js.get("data", [])
        except Exception:
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "report", "force_report": force_report_flag}
        data_list = deduplicate_data(raw_all)
        if not data_list:
            raw_text = f"未查到【{uname}】今日日报记录"
        else:
            raw_text = f"【{uname}{today_str}工作总结】\n"
            for row in data_list:
                raw_text += f"【{row[3]}】\n{row[2]}\n协助：{row[4]}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "report", "force_report": force_report_flag}

    date_pat = r"([\u4e00-\u9fa5]+)(\d{1,2})月(\d{1,2})日工作总结|(\d{1,2})月(\d{1,2})日工作汇报"
    date_match = re.search(date_pat, text)
    if date_match:
        uname = date_match.group(1).strip()
        m = int(date_match.group(2))
        d = int(date_match.group(3))
        target = f"{curr_year}-{m:02d}-{d:02d}"
        try:
            url = f"{API_HOST}/api/query_report?token={TOKEN}&user={uname}&date={target}"
            js = requests.get(url, timeout=5).json()
            raw_all = js.get("data", [])
        except Exception:
            raw_all = []
        data_list = deduplicate_data(raw_all)
        if not data_list:
            raw_text = f"未查到【{uname}】{target}当日日报"
        else:
            raw_text = f"========【{uname}{target}工作总结 】========\n"
            for row in data_list:
                raw_text += f"【{row[3]}】{row[2]}｜协助：{row[4]}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "report", "force_report": force_report_flag}

    meet_day_pat = r"(\d{1,2})月(\d{1,2})[号日]会议记录"
    meet_day_match = re.search(meet_day_pat, text)
    if meet_day_match:
        m = int(meet_day_match.group(1))
        d = int(meet_day_match.group(2))
        target = f"{curr_year}-{m:02d}-{d:02d}"
        try:
            url = f"{API_HOST}/api/getMeetByDate?token={TOKEN}&meet_date={target}"
            js = requests.get(url, timeout=5).json()
            raw_all = js.get("data", [])
        except Exception:
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "meet", "force_report": False}
        data_list = deduplicate_data(raw_all)
        if not data_list:
            raw_text = f"未查询到【{target}】会议记录"
        else:
            raw_text = f"========【{target}会议记录】========\n"
            for row in data_list:
                r_name = row[1]
                r_title = row[2]
                r_date = row[3]
                r_note = row[4]
                raw_text += f"\n【{r_date}｜参会人：{r_name}】\n会议主题：{r_title}\n会议纪要：{r_note}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "meet", "force_report": False}

    meet_week_user_pat = r"([\u4e00-\u9fa5]+)本周参会记录"
    meet_week_match = re.search(meet_week_user_pat, text)
    if meet_week_match:
        uname = meet_week_match.group(1).strip()
        try:
            url = f"{API_HOST}/api/query_meeting?token={TOKEN}&week=now&name={uname}"
            js = requests.get(url, timeout=5).json()
            raw_all = js.get("data", [])
        except Exception:
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "meet", "force_report": False}
        data_list = deduplicate_data(raw_all)
        if not data_list:
            raw_text = f"未查到【{uname}】本周参会记录"
        else:
            raw_text = f"========【{uname}本周参会记录 】========\n"
            for row in data_list:
                raw_text += f"【{row[3]}｜{row[2]}】纪要：{row[4]}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "meet", "force_report": False}

    if "本周全部会议记录" in text or "本周会议记录" in text:
        try:
            url = f"{API_HOST}/api/query_meeting?token={TOKEN}&week=now"
            js = requests.get(url, timeout=5).json()
            raw_all = js.get("data", [])
        except Exception:
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "meet", "force_report": False}
        data_list = deduplicate_data(raw_all)
        if not data_list:
            raw_text = "本周暂无会议记录"
        else:
            raw_text = "========【本周全部会议】========\n"
            for row in data_list:
                raw_text += f"【{row[3]}｜{row[1]}｜{row[2]}】纪要：{row[4]}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "meet", "force_report": False}
    return {"hit": False, "raw_data": "", "raw_list": [], "type": "", "force_report": False}


def llm_parse_question(user_question, force_report_flag):
    if not USE_LLM:
        return {"raw_data": "【Ollama离线，请使用规范语句查询】", "raw_list": []}
    try:
        prompt = f'''分类强制规则：
1. 含【项目、项目进度、项目进展、进展】 → type=project；
2. 含【会议、例会】→type=meet；
3. 其余工作/日报/汇报内容→type=report；
4. 若用户指定具体几月几日，start_date填写对应{curr_year}-MM-DD，没有则空；
仅输出标准JSON{{"type":"project/meet/report","name":"","is_week":true/false,"start_date":""}}，无多余文字。
用户提问：{user_question}'''
        payload = {"model": LLM_MODEL_NAME, "prompt": prompt, "stream": False, "temperature": 0, "num_ctx": 1024}
        res = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT)
        raw = res.json()["response"]
        json_start = raw.find("{")
        json_end = raw.rfind("}")
        if json_start == -1 or json_end == -1:
            return {"raw_data": "【AI解析格式异常，请使用标准查询】", "raw_list": []}
        js_cfg = json.loads(raw[json_start:json_end+1])
        params = {"token": TOKEN}
        name = js_cfg.get("name", "")
        dt = js_cfg.get("start_date", "")
        is_week = js_cfg.get("is_week", False)
        if js_cfg["type"] == "project":
            if is_week:
                url = f"{API_HOST}/api/query_project?token={TOKEN}&week=now"
            elif name:
                url = f"{API_HOST}/api/query_project?token={TOKEN}&name={name}"
            else:
                url = f"{API_HOST}/api/query_project?token={TOKEN}"
            try:
                resp = requests.get(url, timeout=6).json()
            except Exception:
                return {"raw_data": "【接口请求失败】", "raw_list": []}
            data_list = resp.get("data", [])
            if not data_list:
                return {"raw_data": "未查询到相关项目", "raw_list": []}
            out = f"===【{name if name else '全部'}项目清单】===\n"
            for item in data_list:
                out += f"项目：{item[1]}｜负责人：{item[3]}｜进度：{item[7]}｜延期：{item[5]}｜风险：{item[6]}｜更新：{item[8]}\n"
            return {"raw_data": out, "raw_list": data_list}
        elif js_cfg["type"] == "report":
            params["user"] = name
            if is_week:
                params["week"] = "now"
            elif dt:
                params["date"] = dt
            try:
                resp = requests.get(f"{API_HOST}/api/query_report", params=params, timeout=6).json()
            except Exception:
                return {"raw_data": "【接口请求失败】", "raw_list": []}
            arr = resp.get("data", [])
            data_list = deduplicate_data(arr)
        else:
            if is_week:
                if name:
                    params["name"] = name
                    resp = requests.get(f"{API_HOST}/api/query_meeting", params=params, timeout=6).json()
                else:
                    resp = requests.get(f"{API_HOST}/api/query_meeting?token={TOKEN}&week=now", timeout=6).json()
            elif dt:
                resp = requests.get(f"{API_HOST}/api/getMeetByDate?token={TOKEN}&meet_date={dt}", timeout=6).json()
            else:
                return {"raw_data": "无法识别查询日期", "raw_list": []}
            arr = resp.get("data", [])
            data_list = deduplicate_data(arr)
        tag = "日报" if js_cfg["type"] == "report" else "会议"
        if not data_list:
            return {"raw_data": f"未查询到相关{tag}", "raw_list": []}
        out = f"========【{name if name else dt}{tag}】========\n"
        for r in data_list:
            out += f"【{r[3]}｜{r[1]}】{r[2]}｜备注：{r[4]}\n"
        return {"raw_data": out, "raw_list": data_list}
    except Exception:
        return {"raw_data": "【AI解析超时/异常，建议使用标准格式查询】", "raw_list": []}


def llm_make_summary_stream(query_text, data_list):
    if not USE_LLM or not data_list:
        yield "【无有效业务数据】"
        return
    prompt = f"""
70字以内精简总结，提炼核心内容。
项目总结进度；日报总结工作内容；会议总结议题结果。只输出总结正文。
用户查询：{query_text}
原始数据：{json.dumps(data_list, ensure_ascii=False)}
"""
    answer = ""
    try:
        for chunk in ollama_stream(prompt, temperature=0, num_ctx=512):
            answer += chunk
            yield answer
    except Exception:
        yield "总结生成失败"


def user_send_msg(msg, history):
    if not msg.strip():
        return "", history
    history.append({"role": "user", "content": msg})
    return msg, history


def ai_reply(msg, history):
    history.append({"role": "assistant", "content": "🤖 正在分析..."})
    yield history
    if not is_business_query(msg):
        for ans in normal_ai_answer_stream(msg):
            history[-1]["content"] = ans
            yield history
        return

    reg_res = regex_parse_query(msg)
    force_report_flag = reg_res.get("force_report", False)
    if reg_res["hit"]:
        detail = reg_res["raw_data"]
        list_data = reg_res["raw_list"]
    else:
        ai_res = llm_parse_question(msg, force_report_flag)
        detail = ai_res["raw_data"]
        list_data = ai_res["raw_list"]

    temp_text = detail + "\n\n📌 AI正在生成总结..."
    history[-1]["content"] = temp_text
    yield history

    final_text = detail
    for summary in llm_make_summary_stream(msg, list_data):
        final_text = f"""{detail}

=============================================
📌【AI简短总结】
=============================================
{summary}"""
        history[-1]["content"] = final_text
        yield history


# 【核心修复：删除异常过滤代码，正常返回token】
def ollama_stream(prompt, temperature=0.3, num_ctx=1024):
    payload = {
        "model": LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "temperature": temperature,
        "num_ctx": num_ctx
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT, stream=True)
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            obj = json.loads(line)
            chunk = obj.get("response", "")
            if chunk:
                yield chunk
        except:
            continue


def init_welcome():
    return [{"role": "assistant", "content": "您好，欢迎来到工作流查询平台"}]


custom_css = """
*{
    font-family:"Microsoft YaHei","Inter",sans-serif;
    box-sizing:border-box !important;
}
html,body{
    margin:0;padding:0;min-height:100vh;
    overflow-x:hidden !important;overflow-y:auto;
    background:#0b101d;
    background-image:radial-gradient(rgba(30,120,255,.08) 1px,transparent 1px),radial-gradient(rgba(30,120,255,.08) 1px,transparent 1px);
    background-size:25px 25px;
}
.app,.main,.gradio-container{width:100%;}

/* ========== PC ≥901px 严格70%宽度 超高权重 ========== */
@media screen and (min-width:901px){
    html body div.gradio-container{
        width:70% !important;
        max-width:1400px !important;
        min-width:1000px !important;
        margin:0 auto !important;
        padding:18px !important;
    }
}

.header-wrap{
    width:100%;background:linear-gradient(135deg,#04152f,#0a2866,#0f4cb8);
    border-radius:16px;padding:20px 24px;border:1px solid rgba(80,180,255,.35);
    box-shadow:0 0 20px rgba(50,150,255,.35),0 8px 25px rgba(0,0,0,.35);margin-bottom:18px;
}
.header-wrap h1{margin:0;color:white;font-size:28px;}
.header-wrap p{color:#bddcff;margin-top:8px;}
.card-box{
    width:100%;background:linear-gradient(145deg,#101a30,#162848);border-radius:16px;padding:16px;
    border:1px solid rgba(70,170,255,.25);box-shadow:0 0 20px rgba(40,120,255,.15);
}
[data-testid="chatbot"]{width:100% !important;height:70vh !important;}
[data-testid="chatbot"] .message{max-width:85% !important;width:auto !important;}
[data-testid="chatbot"] .message.user{background:linear-gradient(135deg,#0089a8,#00b6c7) !important;color:white !important;border-radius:18px 6px 18px 18px !important;}
[data-testid="chatbot"] .message.bot{background:linear-gradient(135deg,#0a1630,#12264d) !important;color:white !important;border:1px solid rgba(80,140,255,.15) !important;}
[data-testid="chatbot"] .message p{white-space:pre-wrap !important;word-break:break-word !important;overflow-wrap:anywhere !important;line-height:1.7;}
#query-input{width:100%;}
#query-input textarea{background:#0c162c !important;color:#eaf3ff !important;border-radius:14px !important;border:1px solid rgba(80,180,255,.3) !important;min-height:44px !important;font-size:15px !important;}
#query-input textarea:focus{border-color:#39a0ff !important;box-shadow:0 0 0 3px rgba(50,150,255,.2),0 0 20px rgba(50,150,255,.3) !important;}
footer,[data-testid="footer"]{display:none !important;}
::-webkit-scrollbar{width:8px;}
::-webkit-scrollbar-thumb{background:#2d65b8;border-radius:8px;}

/* ========== 手机 ≤900px 固定95% ========== */
@media screen and (max-width:900px){
    html body div.gradio-container{
        width:95% !important;
        max-width:95% !important;
        min-width:0 !important;
        margin:0 auto !important;
        padding:4px !important;
    }
    .header-wrap{padding:12px !important;}
    .header-wrap h1{font-size:20px !important;line-height:1.4 !important;}
    .card-box{padding:6px !important;max-width:100% !important;}
    [data-testid="chatbot"]{height:60vh !important;max-width:100% !important;}
    .gr-box,.gr-form,.gr-input,.gr-button,div[class*="row"],div[class*="column"]{max-width:100% !important;}
}
"""

# 关键修改：fill_width=False
with gr.Blocks(title="AI智能数据中台｜对话查询系统", css=custom_css, fill_width=False) as demo:
    gr.HTML('''
    <div class="header-wrap">
        <h1>🤖 华智瑞森特工作流智能AI查询系统</h1>
        <p>⚡项目进展/进度｜员工日报｜会议纪要 </p>
    </div>
    ''')
    with gr.Column(elem_classes="card-box"):
        chatbot = gr.Chatbot(
            value=init_welcome(),
            height="60vh",
            autoscroll=True,
            render_markdown=True,
            layout="bubble",
            buttons=["copy"],
            avatar_images=("static/user.png", "static/ai.png")
        )
        gr.Markdown("<br>")
        with gr.Row():
            msg = gr.Textbox(
                lines=1,max_lines=3,container=False,show_label=False,
                placeholder="输入查询内容，Enter发送，Shift+Enter换行",elem_id="query-input",label=""
            )
    msg.submit(user_send_msg,[msg,chatbot],[msg,chatbot]).then(ai_reply,[msg,chatbot],[chatbot]).then(lambda:"",None,msg)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7864, share=False)