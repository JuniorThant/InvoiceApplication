
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.base import get_settings

settings = get_settings()

SMTP_SERVER = settings.app.SMTP_SERVER
SMTP_PORT = settings.app.SMTP_PORT
MAILTRAP_USER = settings.app.SMTP_USER
MAILTRAP_PASS = settings.app.SMTP_PASS
SENDER = settings.app.SENDER

"""Send invoice email function"""

def send_invoice_email(to: str, subject: str, html_body: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = to
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(MAILTRAP_USER, MAILTRAP_PASS)
            server.sendmail(SENDER, to, msg.as_string())
        print("Email sent successfully")
    except Exception:
        raise
