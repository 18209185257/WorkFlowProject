import smtplib

from email.mime.text import MIMEText


def send_mail(
        title,
        content,
        to_mail
):

    msg = MIMEText(
        content,
        "html",
        "utf-8"
    )

    msg["Subject"] = title

    msg["From"] = "xxx@qq.com"

    msg["To"] = to_mail

    server = smtplib.SMTP_SSL(
        "smtp.qq.com",
        465
    )

    server.login(
        "xxx@qq.com",
        "授权码"
    )

    server.sendmail(
        "xxx@qq.com",
        [to_mail],
        msg.as_string()
    )

    server.quit()