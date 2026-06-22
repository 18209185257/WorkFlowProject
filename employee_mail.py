import gradio as gr
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

API_HOST = "http://127.0.0.1:8000"
TOKEN = "WorkFlow2026"
today_str = datetime.now().strftime("%Y-%m-%d")

# ==========【企微SMTP配置】==========
MAIL_SMTP = "smtp.exmail.qq.com"
MAIL_PORT = 465
MAIL_SENDER = "zhujintao@szraysent.com"    # 替换为你的企业邮箱
MAIL_PWD = "fjvjgURj6LfgDfDD"           # 替换SMTP授权码
MAIL_TO_DEFAULT = ["leader@xxx.com"]
MAIL_CC_DEFAULT = ["user1@xxx.com","user2@xxx.com"]
# ====================================

def send_qywx_mail(subject, mail_body, to_input, cc_input):
    if to_input and to_input.strip():
        to_list = [x.strip() for x in to_input.split(",") if x.strip()]
    else:
        to_list = MAIL_TO_DEFAULT
    if cc_input and cc_input.strip():
        cc_list = [x.strip() for x in cc_input.split(",") if x.strip()]
    else:
        cc_list = MAIL_CC_DEFAULT

    msg = MIMEText(mail_body, "html", "utf-8")
    # 修复核心：标准Header处理中文标题
    msg['Subject'] = Header(subject, 'utf-8').encode('utf-8')
    msg['From'] = MAIL_SENDER
    msg['To'] = ",".join(to_list)
    if cc_list:
        msg['Cc'] = ",".join(cc_list)

    all_recv = to_list + cc_list
    try:
        server = smtplib.SMTP_SSL(MAIL_SMTP, MAIL_PORT)
        server.login(MAIL_SENDER, MAIL_PWD)
        server.sendmail(MAIL_SENDER, all_recv, msg.as_string())
        server.quit()
        print(f"发送成功 TO:{to_list} CC:{cc_list}")
        return True, ""
    except Exception as e:
        err = str(e)
        print("邮件发送失败：", err)
        return False, err

# 项目提交
def submit_project(name, cycle_start, cycle_end, leader, participants, delay, risk_block, progress, to_str, cc_str):
    cycle = f"{cycle_start} ~ {cycle_end}"
    data = {
        "token": TOKEN,
        "project_name": name,
        "project_cycle": cycle,
        "main_leader": leader,
        "participants": participants,
        "is_delay": delay,
        "risk_block": risk_block,
        "progress": progress
    }
    save_ok = True
    try:
        requests.post(f"{API_HOST}/api/add_project", data=data, timeout=3)
    except Exception as e:
        save_ok = False
        err_msg = str(e)
    if not save_ok:
        return gr.Error(f"后端接口(8000)未启动，数据入库失败：{err_msg}")

    title = f"【项目上报通知】{name}"
    content = f"""
    <h3>项目汇报详情</h3>
    <p>项目名称：{name}</p>
    <p>项目周期：{cycle}</p>
    <p>负责人：{leader}</p>
    <p>参与人：{participants}</p>
    <p>是否延期：{delay}</p>
    <p>风险阻碍：{risk_block}</p>
    <p>进度说明：{progress}</p>
    <p>提交时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """
    mail_ok, mail_err = send_qywx_mail(title, content, to_str, cc_str)
    if mail_ok:
        return gr.Info("✅ 项目提交成功，邮件发送完成！")
    else:
        return gr.Warning(f"✅ 数据保存成功，但邮件发送异常：{mail_err}")

# 会议提交
def submit_meeting(title, sponsor, attendees, meet_date, content, task_problem, to_str, cc_str):
    if not meet_date:
        meet_date = today_str
    data = {
        "token": TOKEN,
        "meet_title": title,
        "sponsor": sponsor,
        "attendees": attendees,
        "meet_date": meet_date,
        "meet_content": content,
        "task_problem": task_problem
    }
    save_ok = True
    try:
        requests.post(f"{API_HOST}/api/add_meeting", data=data, timeout=3)
    except Exception as e:
        save_ok = False
        err_msg = str(e)
    if not save_ok:
        return gr.Error(f"后端接口(8000)未启动，数据入库失败：{err_msg}")

    mail_sub = f"【会议记录上报】{title}"
    mail_body = f"""
    <h3>会议记录详情</h3>
    <p>会议主题：{title}</p>
    <p>发起人：{sponsor}</p>
    <p>参会人员：{attendees}</p>
    <p>会议日期：{meet_date}</p>
    <p>会议内容：{content}</p>
    <p>任务问题：{task_problem}</p>
    <p>提交时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """
    mail_ok, mail_err = send_qywx_mail(mail_sub, mail_body, to_str, cc_str)
    if mail_ok:
        return gr.Info("✅ 会议记录提交成功，邮件发送完成！")
    else:
        return gr.Warning(f"✅ 数据保存成功，但邮件发送异常：{mail_err}")

# 日报提交
def submit_report(reporter, content, report_date, help_item, to_str, cc_str):
    if not report_date:
        report_date = today_str
    data = {
        "token": TOKEN,
        "reporter": reporter,
        "report_content": content,
        "report_date": report_date,
        "help_item": help_item
    }
    save_ok = True
    try:
        requests.post(f"{API_HOST}/api/add_report", data=data, timeout=3)
    except Exception as e:
        save_ok = False
        err_msg = str(e)
    if not save_ok:
        return gr.Error(f"后端接口(8000)未启动，数据入库失败：{err_msg}")

    mail_sub = f"【员工日报】{reporter}-{report_date}"
    mail_body = f"""
    <h3>员工工作日报</h3>
    <p>汇报人：{reporter}</p>
    <p>汇报日期：{report_date}</p>
    <p>日报内容：{content}</p>
    <p>需要协助：{help_item}</p>
    <p>提交时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """
    mail_ok, mail_err = send_qywx_mail(mail_sub, mail_body, to_str, cc_str)
    if mail_ok:
        return gr.Info("✅ 日报提交成功，邮件发送完成！")
    else:
        return gr.Warning(f"✅ 数据保存成功，但邮件发送异常：{mail_err}")

css = """
h2 {
    text-align: center !important;
    font-weight: bold !important;
    color: #0056cc !important;
}
button[aria-selected="true"] {
    color: black !important;
}
button[aria-selected="true"]::after {
    background-color: black !important;
}
"""

with gr.Blocks(title="员工工作上报系统", css=css) as demo:
    gr.Markdown("## 员工工作上报系统")
    with gr.Row():
        input_to_box = gr.Textbox(
            label="收件人邮箱（多个英文逗号分隔，留空使用默认收件）",
            placeholder="admin@xxx.com,leader@xxx.com"
        )
        input_cc_box = gr.Textbox(
            label="抄送邮箱（多个英文逗号分隔，留空使用默认抄送）",
            placeholder="hr@xxx.com,manager@xxx.com"
        )
    with gr.Tabs():
        with gr.TabItem("项目汇报"):
            p_name = gr.Textbox(label="项目名称")
            with gr.Row():
                p_cycle_start = gr.DateTime(label="周期起始日期", type="date", value=today_str, include_time=False)
                p_cycle_end = gr.DateTime(label="周期结束日期", type="date", include_time=False)
            p_leader = gr.Textbox(label="项目主负责人")
            p_part = gr.Textbox(label="参与人及角色")
            p_delay = gr.Radio(["是", "否"], label="是否延期")
            p_risk = gr.Textbox(label="阻碍项、风险项")
            p_progress = gr.Textbox(label="项目进度")
            p_btn = gr.Button("提交", variant="primary")
            p_btn.click(submit_project,[p_name,p_cycle_start,p_cycle_end,p_leader,p_part,p_delay,p_risk,p_progress,input_to_box,input_cc_box])

        with gr.TabItem("会议记录上传"):
            m_title = gr.Textbox(label="会议主题")
            m_sponsor = gr.Textbox(label="发起人")
            m_attend = gr.Textbox(label="参会人")
            m_date = gr.DateTime(label="会议日期", type="date", value=today_str, include_time=False)
            m_content = gr.Textbox(label="会议纪要", lines=6)
            m_task = gr.Textbox(label="Task进展/问题")
            m_btn = gr.Button("提交", variant="primary")
            m_btn.click(submit_meeting,[m_title,m_sponsor,m_attend,m_date,m_content,m_task,input_to_box,input_cc_box])

        with gr.TabItem("日报上传"):
            r_user = gr.Textbox(label="汇报人")
            r_content = gr.Textbox(label="汇报内容（今日总结、明日计划）", lines=8)
            r_date = gr.DateTime(label="汇报日期", type="date", value=today_str, include_time=False)
            r_help = gr.Textbox(label="求助项", lines=3)
            r_btn = gr.Button("提交", variant="primary")
            r_btn.click(submit_report,[r_user,r_content,r_date,r_help,input_to_box,input_cc_box])

demo.launch(
    server_name="127.0.0.1",
    server_port=7863,
    share=False,
    inbrowser=False
)