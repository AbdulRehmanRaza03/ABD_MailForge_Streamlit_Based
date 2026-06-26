import smtplib
import random
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional


def verify_gmail(gmail: str, app_password: str) -> tuple[bool, str]:
    """Verify Gmail credentials"""
    try:
        clean_pass = app_password.replace(" ", "")
        if len(clean_pass) != 16:
            return False, "App Password 16 characters ka hona chahiye"
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(gmail, clean_pass)
        server.quit()
        return True, "Login successful"
    except smtplib.SMTPAuthenticationError:
        return False, "Gmail ya App Password galat hai"
    except Exception as e:
        return False, f"Connection error: {str(e)}"


def send_email(
    gmail: str,
    app_password: str,
    recipient: str,
    subject: str,
    body: str,
    pdf_bytes: Optional[bytes] = None,
    pdf_filename: Optional[str] = None
) -> tuple[bool, str]:
    """Send single email with optional PDF attachment"""
    try:
        clean_pass = app_password.replace(" ", "")
        msg = MIMEMultipart()
        msg["From"] = gmail
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        if pdf_bytes and pdf_filename:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(pdf_bytes)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={pdf_filename}")
            msg.attach(part)

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(gmail, clean_pass)
        server.sendmail(gmail, recipient, msg.as_string())
        server.quit()
        return True, "Sent"

    except smtplib.SMTPRecipientsRefused:
        return False, "Email address invalid"
    except smtplib.SMTPAuthenticationError:
        return False, "Gmail auth failed"
    except Exception as e:
        return False, str(e)


def get_random_interval() -> int:
    """Random delay between 15-45 seconds"""
    return random.randint(15, 45)


def pick_random_template(templates: list) -> tuple[str, str]:
    """Pick random template from list, return (name, body)"""
    if not templates:
        return "None", ""
    chosen = random.choice(templates)
    return chosen.get("name", "Template"), chosen.get("body", "")


def parse_emails_from_text(text: str) -> list[str]:
    """Parse emails from pasted text, one per line"""
    lines = text.strip().split("\n")
    emails = []
    for line in lines:
        email = line.strip().lower()
        if "@" in email and "." in email and len(email) > 5:
            emails.append(email)
    return list(dict.fromkeys(emails))[:400]  # dedupe, max 400
