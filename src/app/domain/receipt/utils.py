import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config._utils import get_env

SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 587
MAILTRAP_USER = "254e5790826d47"
MAILTRAP_PASS = "f74b2140e411aa"
SENDER = "neuraldev@example.com"  


"""Send receipt email function"""
def send_receipt_email(to: str, subject: str, html_body: str):
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
