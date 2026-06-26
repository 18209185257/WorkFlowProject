#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from datetime import datetime, timedelta

API_URL = "http://127.0.0.1:8000/api/query_report"
TOKEN = "WorkFlow2026"

def get_weekly_summary(user="朱金涛"):
    """获取本周工作总结"""
    weekly_data = []
    
    try:
        # 获取本周一到今天的日期
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        
        # 从周一到今天每天查询
        current_date = monday
        while current_date <= today:
            date_str = current_date.strftime("%Y-%m-%d")
            params = {"token": TOKEN, "user": user, "date": date_str}
            
            print(f"正在查询 {date_str} 的数据...")
            resp = requests.get(API_URL, params=params, timeout=10)
            
            if resp.status_code == 200:
                res = resp.json()
                if res.get("code") == 200 and res.get("data"):
                    daily_data = {
                        "date": date_str,
                        "day": current_date.strftime("%A"),
                        "work": res["data"]
                    }
                    weekly_data.append(daily_data)
                else:
                    print(f"{date_str} 无数据")
            else:
                print(f"{date_str} HTTP错误: {resp.status_code}")
            
            current_date += timedelta(days=1)
        
        return weekly_data
        
    except Exception as e:
        print(f"服务异常：{str(e)}")
        return weekly_data

# 获取本周工作总结
weekly_summary = get_weekly_summary("朱金涛")

print("\n朱金涛本周工作总结:")
print("="*50)

if not weekly_summary:
    print("暂无本周工作数据")
else:
    for daily_data in weekly_summary:
        print(f"\nDate: {daily_data['date']} ({daily_data['day']})")
        print("-" * 40)
        for work_item in daily_data['work']:
            if len(work_item) >= 3:
                print(f"- {work_item[2]}")

print("="*50)