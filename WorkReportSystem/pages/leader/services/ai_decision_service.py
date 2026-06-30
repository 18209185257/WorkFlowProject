import requests
import json
from common.db import OLLAMA_URL,MODEL_NAME,get_project_conn

def call_ollama(prompt, model="llama3"):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    res = requests.post(OLLAMA_URL, json=payload)
    return res.json().get("response", "")

#构建经营数据（关键）
def get_business_context():

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("select count(*) from project")
    project_count = cur.fetchone()[0]

    cur.execute("select count(*) from customer")
    customer_count = cur.fetchone()[0]

    cur.execute("select count(*) from daily_report")
    report_count = cur.fetchone()[0]

    cur.execute("""
        select risk_level, count(*)
        from project
        group by risk_level
    """)
    risk_data = cur.fetchall()

    conn.close()

    return {

        "project_count": project_count,

        "customer_count": customer_count,

        "report_count": report_count,

        "risk_data": risk_data

    }

#构建Prompt（核心）
def build_decision_prompt(data):

    risk_text = "\n".join([
        f"{r[0]}: {r[1]}个项目"
        for r in data["risk_data"]
    ])

    prompt = f"""
你是企业AI经营决策系统，请基于以下数据做分析：

项目总数：{data['project_count']}
客户总数：{data['customer_count']}
日报总数：{data['report_count']}

风险分布：
{risk_text}

请输出：

1、当前经营状况总结
2、存在的主要问题
3、风险判断
4、关键改进建议（3-5条）
5、下一步行动计划

要求：
- 简洁
- 面向企业管理层
- 可执行
"""

    return prompt

#主函数（AI决策）
def build_ai_decision(username):

    data = get_business_context()

    prompt = build_decision_prompt(data)

    result = call_ollama(prompt)

    return f"""
### 🧠 AI经营决策报告

---

{result}
"""

