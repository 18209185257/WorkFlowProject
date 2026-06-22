from datetime import datetime

# =============================
# API配置
# =============================

API_HOST = "http://127.0.0.1:8000"

TOKEN = "WorkFlow2026"

# =============================
# Ollama配置
# =============================

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

OLLAMA_TAG_URL = "http://127.0.0.1:11434/api/tags"

LLM_MODEL_NAME = "deepseek-r1:8b"

OLLAMA_TIMEOUT = 25

# =============================
# 时间配置
# =============================

TODAY_STR = datetime.now().strftime("%Y-%m-%d")

CURR_YEAR = datetime.now().year

# =============================
# 业务关键词
# =============================

BUSINESS_KEYWORDS = [
    "项目",
    "进度",
    "项目进展",
    "进展",
    "日报",
    "工作总结",
    "工作汇报",
    "汇报",
    "工作内容",
    "明日计划",
    "会议",
    "参会",
    "会议记录",
    "例会",
    "工作",
    "总结",
    "工作计划"
]
