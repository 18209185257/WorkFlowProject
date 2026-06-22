import re
import json
import requests
from datetime import datetime

from ..leader_config import (
    API_HOST,
    TOKEN,
    TODAY_STR,
    CURR_YEAR,
    OLLAMA_URL,
    LLM_MODEL_NAME,
    OLLAMA_TIMEOUT,
    BUSINESS_KEYWORDS
)

from ..utils.data_utils import deduplicate_data
from .ollama_service import USE_LLM

today_str = datetime.now().strftime("%Y-%m-%d")
curr_year = datetime.now().year

def is_business_query(text):

    for kw in BUSINESS_KEYWORDS:
        if kw in text:
            return True

    if re.search(
        r"\d{1,2}[月号日].*(总结|日报|工作|汇报)",
        text
    ):
        return True

    if re.search(
        r"[\u4e00-\u9fa5]{2,}.*(总结|日报|汇报)",
        text
    ):
        return True

    return False


def regex_parse_query(text):

    # =====================================
    # 项目查询
    # =====================================

    single_proj_pat = r"([\u4e00-\u9fa5]+)(项目进度|项目进展|进展|进度)"

    single_proj_match = re.search(
        single_proj_pat,
        text
    )

    if single_proj_match:

        proj_name = single_proj_match.group(1).strip()

        url = (
            f"{API_HOST}/api/query_project"
            f"?token={TOKEN}"
            f"&name={proj_name}"
        )

        try:

            res = requests.get(
                url,
                timeout=5
            )

            js = res.json()

            data_list = js.get("data", [])

        except Exception:

            return {
                "hit": True,
                "raw_data": "【后端接口请求失败，请检查服务是否开启】",
                "raw_list": [],
                "type": "project",
                "force_report": False
            }

        if not data_list:

            raw_text = f"未找到【{proj_name}】相关项目"

        else:

            raw_text = f"===【{proj_name}】项目详情===\n"

            for item in data_list:

                raw_text += (
                    f"项目：{item[1]}｜"
                    f"周期：{item[2]}｜"
                    f"负责人：{item[3]}｜"
                    f"延期：{item[5]}｜"
                    f"风险：{item[6]}｜"
                    f"进度：{item[7]}｜"
                    f"更新：{item[8]}\n"
                )

        return {
            "hit": True,
            "raw_data": raw_text,
            "raw_list": data_list,
            "type": "project",
            "force_report": False
        }

    # =====================================
    # 本周项目
    # =====================================

    if (
        "本周项目进度" in text
        or "本周项目进展" in text
        or "本周进展" in text
    ):

        try:

            js = requests.get(
                f"{API_HOST}/api/query_project?token={TOKEN}&week=now",
                timeout=5
            ).json()

            data_list = js.get("data", [])

        except Exception:

            return {
                "hit": True,
                "raw_data": "【后端接口请求失败，请检查服务是否开启】",
                "raw_list": [],
                "type": "project",
                "force_report": False
            }

        if not data_list:

            raw_text = "本周暂无更新项目"

        else:

            raw_text = "===本周更新项目清单===\n"

            for item in data_list:

                raw_text += (
                    f"项目：{item[1]}｜"
                    f"负责人：{item[3]}｜"
                    f"进度：{item[7]}｜"
                    f"延期：{item[5]}｜"
                    f"风险：{item[6]}｜"
                    f"更新时间：{item[8]}\n"
                )

        return {
            "hit": True,
            "raw_data": raw_text,
            "raw_list": data_list,
            "type": "project",
            "force_report": False
        }

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
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "report",
                    "force_report": force_report_flag}
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
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "report",
                "force_report": force_report_flag}

    day_pat = r"([\u4e00-\u9fa5]+)今日工作总结|今日工作汇报"
    day_match = re.search(day_pat, text)
    if day_match:
        uname = day_match.group(1).strip()
        url = f"{API_HOST}/api/query_report?token={TOKEN}&user={uname}&date={today_str}"
        try:
            js = requests.get(url, timeout=5).json()
            raw_all = js.get("data", [])
        except Exception:
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "report",
                    "force_report": force_report_flag}
        data_list = deduplicate_data(raw_all)
        if not data_list:
            raw_text = f"未查到【{uname}】今日日报记录"
        else:
            raw_text = f"【{uname}{today_str}工作总结】\n"
            for row in data_list:
                raw_text += f"【{row[3]}】\n{row[2]}\n协助：{row[4]}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "report",
                "force_report": force_report_flag}

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
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "report",
                "force_report": force_report_flag}

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
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "meet",
                    "force_report": False}
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
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "meet",
                    "force_report": False}
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
            return {"hit": True, "raw_data": "【后端接口请求失败，请检查服务是否开启】", "raw_list": [], "type": "meet",
                    "force_report": False}
        data_list = deduplicate_data(raw_all)
        if not data_list:
            raw_text = "本周暂无会议记录"
        else:
            raw_text = "========【本周全部会议】========\n"
            for row in data_list:
                raw_text += f"【{row[3]}｜{row[1]}｜{row[2]}】纪要：{row[4]}\n"
        return {"hit": True, "raw_data": raw_text, "raw_list": data_list, "type": "meet", "force_report": False}
    return {"hit": False, "raw_data": "", "raw_list": [], "type": "", "force_report": False}

def llm_parse_question(
        user_question,
        force_report_flag=False
):

    if not USE_LLM:

        return {
            "raw_data": "【Ollama离线】",
            "raw_list": []
        }

    try:

        prompt = f"""
分类强制规则：

1. 含项目/项目进度/项目进展
→ type=project

2. 含会议/例会
→ type=meet

3. 其余工作/日报/汇报
→ type=report

4. 若用户指定日期：
返回 YYYY-MM-DD

仅输出JSON：

{{
"type":"project|meet|report",
"name":"",
"is_week":false,
"start_date":""
}}

用户问题：
{user_question}
"""

        payload = {
            "model": LLM_MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "temperature": 0,
            "num_ctx": 1024
        }

        res = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        raw = res.json()["response"]

        json_start = raw.find("{")
        json_end = raw.rfind("}")

        js_cfg = json.loads(
            raw[json_start:json_end + 1]
        )

        name = js_cfg.get("name", "")
        dt = js_cfg.get("start_date", "")
        is_week = js_cfg.get("is_week", False)

        # ===================
        # 项目查询
        # ===================

        if js_cfg["type"] == "project":

            if is_week:

                url = (
                    f"{API_HOST}/api/query_project"
                    f"?token={TOKEN}&week=now"
                )

            elif name:

                url = (
                    f"{API_HOST}/api/query_project"
                    f"?token={TOKEN}&name={name}"
                )

            else:

                url = (
                    f"{API_HOST}/api/query_project"
                    f"?token={TOKEN}"
                )

            resp = requests.get(
                url,
                timeout=10
            ).json()

            data_list = resp.get(
                "data",
                []
            )

            if not data_list:

                return {
                    "raw_data": "未查询到相关项目",
                    "raw_list": []
                }

            out = "===项目查询结果===\n"

            for item in data_list:

                out += (
                    f"项目：{item[1]}｜"
                    f"负责人：{item[3]}｜"
                    f"进度：{item[7]}｜"
                    f"延期：{item[5]}｜"
                    f"风险：{item[6]}\n"
                )

            return {
                "raw_data": out,
                "raw_list": data_list
            }

        # ===================
        # 日报查询
        # ===================

        elif js_cfg["type"] == "report":

            params = {
                "token": TOKEN
            }

            if name:
                params["user"] = name

            if dt:
                params["date"] = dt

            if is_week:
                params["week"] = "now"

            resp = requests.get(
                f"{API_HOST}/api/query_report",
                params=params,
                timeout=10
            ).json()

            data_list = deduplicate_data(
                resp.get("data", [])
            )

        # ===================
        # 会议查询
        # ===================

        else:

            if dt:

                resp = requests.get(
                    f"{API_HOST}/api/getMeetByDate",
                    params={
                        "token": TOKEN,
                        "meet_date": dt,
                        "name": name
                    },
                    timeout=10
                ).json()

            elif is_week:

                resp = requests.get(
                    f"{API_HOST}/api/query_meeting",
                    params={
                        "token": TOKEN,
                        "week": "now"
                    },
                    timeout=10
                ).json()

            else:

                return {
                    "raw_data": "无法识别会议日期",
                    "raw_list": []
                }

            data_list = deduplicate_data(
                resp.get("data", [])
            )

        # ===================
        # 输出结果
        # ===================

        if not data_list:

            return {
                "raw_data": "未查询到相关记录",
                "raw_list": []
            }

        tag = (
            "日报"
            if js_cfg["type"] == "report"
            else "会议"
        )

        out = f"==== {tag}查询结果 ====\n"

        for r in data_list:

            out += (
                f"【{r[3]}】"
                f"{r[1]} "
                f"{r[2]}\n"
            )

        return {
            "raw_data": out,
            "raw_list": data_list
        }

    except Exception as e:

        print("OLLAMA ERROR =", e)

        return {
            "raw_data":
                f"【AI解析异常】{str(e)}",
            "raw_list": []
        }
