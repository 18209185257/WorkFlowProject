from ..ollama_service import (
  USE_LLM,
  ollama_stream
)

def llm_make_summary_stream(
    question,
    raw_list
    ):

    if not USE_LLM:

        yield "AI离线"

        return
    report_text = ""
    for row in raw_list:
        report_text += f"""
    日期：{row[3]}

    工作内容：
    {row[2]}

    需协助：
    {row[4]}
    """

    prompt = f"""
你是一名企业项目经理。

下面是员工本周日报内容：

{report_text}

请严格按照以下格式输出：

【本周重点】
总结3条以内最重要工作成果。

【风险分析】
列出可能延期、阻塞、依赖风险。
没有风险写：
暂无明显风险。

【管理建议】
给项目经理的建议。

要求：

1. 不要复述原文
2. 不要重复内容
3. 控制在150字以内
4. 用中文
"""

    answer = ""

    try:

        for chunk in ollama_stream(
                prompt,
                temperature=0.7,
                num_ctx=4096,
        ):

            answer += chunk

            yield answer

    except Exception:

        yield "AI总结失败"

