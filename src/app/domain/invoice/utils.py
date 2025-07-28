import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config._utils import get_env

SMTP_SERVER = get_env("SMTP_SERVER", default="")()
SMTP_PORT = int(get_env("SMTP_PORT", default="587")())
MAILTRAP_USER = get_env("MAILTRAP_USER", default="")()
MAILTRAP_PASS = get_env("MAILTRAP_PASS", default="")()
SENDER = get_env("SENDER", default="")()


"""Send invoice email function"""
def send_invoice_email(to: str, subject: str, html_body: str):
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
        print("Email sent successfully.")
    except Exception as e:
        print(f"Email send failed: {e}")
