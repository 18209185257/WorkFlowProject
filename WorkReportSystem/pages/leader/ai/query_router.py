from .services.report_service import *
from .services.project_service import *
from .services.meeting_service import *
from  .services.llm_service import *

def dispatch_query(text):
    print("QUERY =", text)
    text=text.strip()
    # ===================== # 日报 # =====================
    if "本周工作统计" in text:
        return query_work_statistics()
    if "日报排行榜" in text:
        return query_daily_rank()
    if "最近日报" in text:
        return query_user_recent_report(text)
    if "本周日报" in text:
        return query_user_week_report(text)
    if "本周工作总结" in text:
        return query_user_week_report(text)
    if "今日工作总结" in text:
        return query_user_today_report(text)
    # ===================== # 项目 # =====================
    if "项目排行" in text:
        return query_project_rank()
    if "项目统计" in text:
        return query_project_statistics()
    if "本周项目" in text:
        return query_week_project()
    if  "项目进度" in text or "项目进展" in text :
        return query_all_project()
    # ===================== # 会议 # =====================
    if "会议统计" in text:
        return query_meeting_statistics()
    if "会议排行" in text:
        return query_meeting_rank()
    if "本周会议记录" in text:
        return query_week_meeting()
    if "本周参会记录" in text:
        return query_user_week_meeting(text)
    if "会议记录" in text:
        return query_meeting_by_date(text)
    return { "raw_data":"暂未识别该查询", "raw_list":[] }