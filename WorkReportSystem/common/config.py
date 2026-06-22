from pathlib import Path
from datetime import datetime


API_HOST = "http://127.0.0.1:8000"

TOKEN = "WorkFlow2026"

TODAY = datetime.now().strftime("%Y-%m-%d")

CURR_YEAR = datetime.now().year

# WorkReportSystem 根目录
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "workflow.db"

DB_USER_PATH = BASE_DIR / "database" / "user.db"

