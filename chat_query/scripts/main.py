import requests
import re
from datetime import datetime

TOKEN = "WorkFlow2026"
BASE_URL = "http://127.0.0.1:8000"
today = datetime.now().strftime("%Y-%m-%d")
curr_year = datetime.now().year

def on_message(text):
    print("====进入技能脚本====", text)

    # ==========【新增：指定某日全量会议/某人某日会议】核心修复代码==========
    # 匹配三种句式：5月30会议、朱金涛5月30会议、5月30朱金涛会议
    day_meet_pat = r"(?:([\u4e00-\u9fa5]{2,6}))?(\d{1,2})月(\d{1,2})号?的?([\u4e00-\u9fa5]{2,6})?会议记录"
    day_meet_match = re.search(day_meet_pat, text)
    if day_meet_match:
        name1 = day_meet_match.group(1) or ""
        name2 = day_meet_match.group(4) or ""
        m = int(day_meet_match.group(2))
        d = int(day_meet_match.group(3))
        target_day = f"{curr_year}-{m:02d}-{d:02d}"
        # 合并两个位置提取的人名
        real_name = (name1+name2).strip()
        # 拼接专用会议接口getMeetByDate
        url = f"{BASE_URL}/api/getMeetByDate?token={TOKEN}&meet_date={target_day}"
        if real_name:
            url += f"&name={real_name}"
        resp = requests.get(url,timeout=5).json()
        all_meet = resp.get("data",[])
        if not all_meet:
            return f"{target_day}无相关会议记录"
        out = f"【{target_day}会议记录】\n"
        for m_item in all_meet:
            out += f"{m_item[4]} | 主题:{m_item[1]} | 发起人:{m_item[2]} | 参会:{m_item[3]} | 纪要:{m_item[5]}\n"
        return out

    # ==========新增：按人名查本周参会 / 某月参会==========
    # 1.本周参会：朱金涛本周参会记录
    week_meet_pat = r"([\u4e00-\u9fa5]{2,6})本周参会记录"
    week_meet_match = re.search(week_meet_pat, text)
    if week_meet_match:
        name = week_meet_match.group(1)
        # 获取本周全部会议
        url = f"{BASE_URL}/api/query_meeting?token={TOKEN}&week=now"
        resp = requests.get(url,timeout=5).json()
        all_meet = resp.get("data",[])
        out = f"【{name}本周参会记录】\n"
        has = False
        for m in all_meet:
            meet_date = m[4]
            attend = m[3]
            if name in attend:
                has = True
                out += f"{meet_date} | {m[1]} | 发起人:{m[2]} | 纪要:{m[5]}\n"
        if not has:
            out += "本周无参会记录"
        return out

    # 2.某月参会：朱金涛6月参会记录
    month_meet_pat = r"([\u4e00-\u9fa5]{2,6})(\d{1,2})月参会记录"
    month_meet_match = re.search(month_meet_pat, text)
    if month_meet_match:
        name = month_meet_match.group(1)
        mon = int(month_meet_match.group(2))
        target_month = f"{curr_year}-{mon:02d}"
        # 取全部会议，前端筛选年月
        resp = requests.get(f"{BASE_URL}/api/query_meeting?token={TOKEN}",timeout=5).json()
        all_meet = resp.get("data",[])
        out = f"【{name}{mon}月参会记录】\n"
        has = False
        for m in all_meet:
            meet_date = m[4]
            attend = m[3]
            if meet_date.startswith(target_month) and name in attend:
                has = True
                out += f"{meet_date} | {m[1]} | 发起人:{m[2]} | 纪要:{m[5]}\n"
        if not has:
            out += f"{mon}月无参会记录"
        return out

    # 原有：某日日报+参会两种语序
    mix_pat = r"([\u4e00-\u9fa5]{2,6})(\d{1,2})月(\d{1,2})日(参会记录和工作总结|工作总结和参会记录)"
    mix_match = re.search(mix_pat, text)
    if mix_match:
        name = mix_match.group(1)
        m = int(mix_match.group(2))
        d = int(mix_match.group(3))
        target_day = f"{curr_year}-{m:02d}-{d:02d}"
        out_text = f"====【{name} {target_day}工作汇总】====\n"

        rep_url = f"{BASE_URL}/api/query_report?token={TOKEN}&user={name}&date={target_day}"
        rep_resp = requests.get(rep_url,timeout=5).json()
        rep_list = rep_resp.get("data",[])
        out_text += "【当日工作总结】\n"
        if rep_list:
            out_text += f"{rep_list[0][2]}\n求助项：{rep_list[0][4]}\n"
        else:
            out_text += "无当日日报\n"

        meet_url = f"{BASE_URL}/api/query_meeting?token={TOKEN}"
        meet_resp = requests.get(meet_url,timeout=5).json()
        all_meet = meet_resp.get("data",[])
        out_text += "\n【当日参会记录】\n"
        flag = False
        for item in all_meet:
            meet_date = item[4]
            attend_users = item[3]
            if meet_date == target_day and name in attend_users:
                flag = True
                out_text += f"会议主题：{item[1]}｜发起人：{item[2]}\n纪要：{item[5]}\n"
        if not flag:
            out_text += "当日无参会记录\n"
        return out_text

    # 单人指定某天日报
    date_pat = r"([\u4e00-\u9fa5]{2,6})(\d{1,2})月(\d{1,2})日工作总结"
    date_match = re.search(date_pat, text)
    if date_match:
        uname = date_match.group(1)
        mon = int(date_match.group(2))
        day = int(date_match.group(3))
        target_date = f"{curr_year}-{mon:02d}-{day:02d}"
        url = f"{BASE_URL}/api/query_report?token={TOKEN}&user={uname}&date={target_date}"
        js = requests.get(url, timeout=5).json()
        data_list = js.get("data", [])
        if not data_list:
            return f"未查到【{uname}】{target_date}日报"
        row = data_list[0]
        return f"【{uname} {target_date}工作总结】\n{row[2]}\n求助：{row[4]}"

    # 单人本周日报
    week_user_pat = r"([\u4e00-\u9fa5]{2,6})本周工作总结"
    week_user_match = re.search(week_user_pat, text)
    if week_user_match:
        uname = week_user_match.group(1)
        url = f"{BASE_URL}/api/query_report?token={TOKEN}&user={uname}&week=now"
        js = requests.get(url, timeout=5).json()
        data_list = js.get("data", [])
        if not data_list:
            return f"未查到【{uname}】本周日报记录"
        out = f"【{uname}本周工作总结汇总】\n"
        for row in data_list:
            out += f"{row[3]}：\n{row[2]}\n求助项：{row[4]}\n------\n"
        return out

    # 单人当日日报
    day_pat = r"([\u4e00-\u9fa5]{2,6})(今日)?工作总结"
    day_match = re.search(day_pat, text)
    if day_match:
        uname = day_match.group(1)
        url = f"{BASE_URL}/api/query_report?token={TOKEN}&user={uname}&date={today}"
        js = requests.get(url, timeout=5).json()
        data_list = js.get("data", [])
        if not data_list:
            return f"未查到【{uname}】今日日报记录"
        row = data_list[0]
        return f"【{uname}今日工作总结】\n{row[2]}\n求助事项：{row[4]}"

    # 本周全部会议
    if "本周会议" in text or "本周全部会议记录" in text:
        url = f"{BASE_URL}/api/query_meeting?token={TOKEN}&week=now"
        js = requests.get(url, timeout=5).json()
        data_list = js.get("data", [])
        if not data_list:
            return "本周暂无会议记录"
        tmp = "===本周会议清单===\n"
        for item in data_list:
            tmp += f"{item[4]}｜{item[1]}｜发起人:{item[2]}｜参会:{item[3]}｜纪要：{item[5]}\n"
        return tmp

    # 全部会议
    if "会议记录" in text:
        url = f"{BASE_URL}/api/query_meeting?token={TOKEN}"
        js = requests.get(url, timeout=5).json()
        data_list = js.get("data", [])
        if not data_list:
            return "暂无会议记录"
        tmp = "===全部会议记录===\n"
        for item in data_list:
            tmp += f"{item[4]}｜{item[1]}｜发起人:{item[2]}｜参会:{item[3]}｜纪要：{item[5]}\n"
        return tmp

    # 单项目名称查询
    single_proj_pat = r"([\u4e00-\u9fa5]+)项目进度"
    single_proj_match = re.search(single_proj_pat, text)
    if single_proj_match:
        proj_name = single_proj_match.group(1)
        url = f"{BASE_URL}/api/query_project?token={TOKEN}&name={proj_name}"
        res = requests.get(url, timeout=5)
        js = res.json()
        data_list = js.get("data", [])
        if not data_list:
            return f"未找到【{proj_name}】相关项目"
        tmp = f"===【{proj_name}】项目详情===\n"
        for item in data_list:
            tmp += f"项目：{item[1]}｜周期：{item[2]}｜负责人：{item[3]}｜延期：{item[5]}｜风险：{item[6]}｜进度：{item[7]}｜更新：{item[8]}\n"
        return tmp

    # 本周更新项目
    if "本周项目进度" in text:
        url = f"{BASE_URL}/api/query_project?token={TOKEN}&week=now"
        js = requests.get(url, timeout=5).json()
        data_list = js.get("data", [])
        if not data_list:
            return "本周暂无更新项目"
        tmp = "===本周更新项目清单===\n"
        for item in data_list:
            tmp += f"项目：{item[1]}｜负责人：{item[3]}｜进度：{item[7]}｜延期：{item[5]}｜风险：{item[6]}｜更新时间：{item[8]}\n"
        return tmp

    # 全部项目
    if "项目进度" in text:
        url = f"{BASE_URL}/api/query_project?token={TOKEN}"
        js = requests.get(url, timeout=5).json()
        data_list = js.get("data", [])
        if not data_list:
            return "暂无项目记录"
        tmp = "===全部项目清单===\n"
        for item in data_list:
            tmp += f"项目：{item[1]}｜负责人：{item[3]}｜进度：{item[7]}｜延期：{item[5]}｜风险：{item[6]}｜更新时间：{item[8]}\n"
        return tmp

    # 当日全量汇总
    if "今日汇总" in text or "工作简报" in text:
        url = f"{BASE_URL}/api/today_summary?token={TOKEN}"
        js = requests.get(url, timeout=5).json()
        return js.get("data","暂无汇总数据")

    return """可用指令：
【日报】
查询XXX工作总结｜查询XXX本周工作总结｜查询XXX6月1日工作总结
查询XXX6月1日参会记录和工作总结｜查询XXX6月1日工作总结和参会记录
【个人参会新增】
查询XXX本周参会记录｜查询XXX6月参会记录｜查询5月30号会议记录｜查询朱金涛5月30号会议记录
【公共会议】
查询会议记录｜查询本周全部会议记录
【项目】
查询项目进度｜查询本周项目进度｜查询XX项目进度
【汇总】查询今日汇总"""