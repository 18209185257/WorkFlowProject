#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

API_URL = "http://127.0.0.1:8000/api/getMeetByDate"
TOKEN = "***"

def get_meeting_record(date="5月30"):
    try:
        params = {"token": TOKEN, "meet_date": date}
        resp = requests.get(API_URL, params=params, timeout=5)
        if resp.status_code == 200:
            res = resp.json()
            if res.get("code") == 200 and res.get("data"):
                return json.dumps(res["data"], ensure_ascii=False, indent=2)
        return "查询失败"
    except Exception as e:
        return f"服务异常：{str(e)}"

result = get_meeting_record("5月30")
print(result)