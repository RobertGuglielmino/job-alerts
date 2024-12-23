
from datetime import datetime
from email.message import EmailMessage
from email.mime.text import MIMEText
import os
import smtplib
import ssl
from typing import Dict, List

def send_email(subject: str, body: str):
    email_file = _load_file_lines(f"config/email.txt")
    email = email_file[0]  # First line is email
    app_pw = email_file[1]  # Second line is application password
    print(f"sending email to {email}")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email 
    msg['To'] = email

    # Configure your SMTP settings
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email, app_pw)
            server.send_message(msg)
    except Exception as e:
        print(f"could not send email: {e}")


def format_jobs_email(new_jobs: List[Dict[str, str]]):

    if len(new_jobs) == 0:
        return

    msg_body = ""
    for job in new_jobs:
        msg_body += f"{job['title']}: {job['url']}\n\n"

    send_email('it\'s job time', msg_body)


def format_string_email(msg_body):
    send_email('cant parse page', msg_body)

        
def _load_file_lines(filename: str) -> List[str]:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

