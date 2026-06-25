from .ai_memory_service import save_conversation,build_ai_context,clean_old_conversation
import requests
from .hybrid_rag_service import (
    hybrid_search
)
from common.db import OLLAMA_URL

from .model_router import (
    get_model
)

from .ollama_service import (
    call_model
)

def generate_ai_chat(username, question):

    save_conversation(
        username,
        "user",
        question
    )

    clean_old_conversation(
        username
    )

    memory_context = build_ai_context(
        username
    )

    rag_docs = hybrid_search(
        question,
        top_k=8
    )

    rag_context = ""

    for doc in rag_docs:
        rag_context += \
            doc + "\n\n"

    prompt = f"""
    你是企业工作汇报平台AI助手。

    回答规则：

    1、优先依据知识库内容回答

    2、知识库没有内容时，
    使用你自己的知识回答

    3、保持上下文连续性

    历史对话：

    {memory_context}

    知识库检索结果：

    {rag_context}
    
    回答要求：
    
    1.优先依据知识库回答
    
    2.知识库没有时，
    再使用你自己的知识
    
    3.不要编造项目数据
    
    4.项目名称、
    人员姓名、
    客户名称、
    编号
    必须严格依据知识库

    用户问题：

    {question}

    请开始回答：
    """

    model = get_model(
        "chat"
    )

    answer = call_model(
        model,
        prompt
    )

    save_conversation(
        username,
        "assistant",
        answer
    )

    clean_old_conversation(
        username
    )

    return answer