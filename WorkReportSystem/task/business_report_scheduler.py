from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from pages.leader.services.auto_business_report_service import (
    generate_daily_business_report
)

from common.email_sender import (
    send_mail
)


def auto_report_job():

    report = generate_daily_business_report()

    send_mail(

        "AI经营日报",

        report,

        "boss@qq.com"

    )


def start_scheduler():

    scheduler = (
        BackgroundScheduler()
    )

    scheduler.add_job(

        auto_report_job,

        "cron",

        hour=8,

        minute=0

    )

    scheduler.start()