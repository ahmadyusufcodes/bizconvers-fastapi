import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from os import environ

GMAIL_USER = environ.get("GMAIL_USER")
GMAIL_PASS = environ.get("GMAIL_PASS")

def send_email(subject, body, recipients):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(GMAIL_USER, GMAIL_PASS)
       smtp_server.sendmail(GMAIL_USER, recipients, msg.as_string())
    smtp_server.close()
