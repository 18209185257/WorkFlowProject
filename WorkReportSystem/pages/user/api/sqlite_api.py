from fastapi import FastAPI
import sqlite3

app = FastAPI()


def conn():
    return sqlite3.connect("workflow.db")


@app.get("/api/kpi")
def kpi(user: str):

    c = conn().cursor()

    report = c.execute(
        "select count(*) from daily_report where reporter=?",
        (user,)
    ).fetchone()[0]

    meeting = c.execute(
        "select count(*) from meeting where sponsor=?",
        (user,)
    ).fetchone()[0]

    project = c.execute("""
        select count(*) from project
        where main_leader like ?
           or developers like ?
           or testers like ?
           or designer like ?
    """, (f"%{user}%",)*4).fetchone()[0]

    return {
        "report": report,
        "meeting": meeting,
        "project": project
    }


@app.get("/api/pie")
def pie(user: str):

    k = kpi(user)

    return k


@app.get("/api/line")
def line(user: str):

    c = conn().cursor()

    rows = c.execute("""
        select submit_date, count(*)
        from daily_report
        where reporter=?
        group by submit_date
        order by submit_date
        limit 7
    """, (user,)).fetchall()

    return [
        {"date": r[0], "count": r[1]}
        for r in rows
    ]