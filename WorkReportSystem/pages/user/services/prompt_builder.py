from .ai_memory_service import build_ai_context
from .rag.chroma_service import (
    search_docs
)


def build_prompt(
        username,
        question
):

    docs = search_docs(
        question
    )

    rag_context = "\n".join(
        docs
    )

    memory_context = build_ai_context(
        username
    )

    return f"""
你是企业AI助手

历史记忆：

{memory_context}

知识库内容：

{rag_context}

用户问题：

{question}

请优先依据知识库回答。
如果知识库不足，
再使用你的推理能力补充。
"""