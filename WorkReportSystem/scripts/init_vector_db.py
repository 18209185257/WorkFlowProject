from pages.user.services.rag.vector_sync import *

sync_daily_reports()

sync_project_reports()

print(
    "向量库初始化完成"
)