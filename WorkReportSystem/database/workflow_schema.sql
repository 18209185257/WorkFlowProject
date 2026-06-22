CREATE TABLE IF NOT EXISTS daily_reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    report_date TEXT,
    today_work TEXT,
    tomorrow_plan TEXT,
    help_needed TEXT
);

CREATE TABLE IF NOT EXISTS meeting_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_title TEXT,
    meeting_date TEXT,
    content TEXT
);

CREATE TABLE IF NOT EXISTS project_reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT,
    progress TEXT,
    risk TEXT,
    next_plan TEXT
);