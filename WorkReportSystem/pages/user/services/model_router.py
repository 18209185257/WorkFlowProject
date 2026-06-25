MODEL_MAP = {

    "daily": "qwen2.5:7b",

    "weekly": "qwen2.5:7b",

    "meeting": "qwen2.5:7b",

    "chat": "qwen2.5:7b",

    "project": "deepseek-r1:8b",

    "risk": "deepseek-r1:8b",

    "master": "deepseek-r1:8b"
}

def get_model(task):

    return MODEL_MAP.get(
        task,
        "qwen2.5:7b"
    )
