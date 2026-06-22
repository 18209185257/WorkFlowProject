from .query_router import dispatch_query

from .llm.intent_service import (
    llm_parse_question
)

from .services.summary_service import (
    llm_make_summary_stream
)

def user_send_msg(msg, history):
    history = history or []

    history.append(
        {
            "role": "user",
            "content": msg
        }
    )

    print(history)
    print(type(history))
    print(type(history[0]))
    return "", history

def ai_reply(history):

    if not history:
        yield history
        return

    msg = history[-1]["content"]

    history.append({
        "role":"assistant",
        "content":"🤖 正在分析..."
    })

    yield history

    result = dispatch_query(msg)

    detail = result["raw_data"]
    rows = result["raw_list"]

    history[-1]["content"] = detail

    yield history

    if rows:

        summary_text = ""

        for chunk in llm_make_summary_stream(
            msg,
            rows
        ):

            summary_text += chunk

            history[-1]["content"] = (
                detail
                + "\n\n"
                + "====================\n"
                + "📌 AI总结\n"
                + "====================\n"
                + summary_text
            )

            yield history

def init_welcome():
    """返回欢迎消息，使用messages格式"""
    return [
        {
            "role": "assistant",
            "content": "您好，欢迎来到工作流查询平台"
        }
    ]
