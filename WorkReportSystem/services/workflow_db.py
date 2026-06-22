import sqlite3
from database.db_config import WORKFLOW_DB


def get_conn():
    return sqlite3.connect(WORKFLOW_DB)