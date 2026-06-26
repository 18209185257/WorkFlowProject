import requests
API_URL = "http://127.0.0.1:8000/api/today_summary"
TOKEN = "WorkFlow2026"

def main(args):
    try:
        params = {"token": TOKEN}
        resp = requests.get(API_URL, params=params, timeout=20)
        res = resp.json()
        return res["data"] if res["code"] == 200 else "数据查询失败"
    except Exception as e:
        return f"服务异常：{str(e)}"