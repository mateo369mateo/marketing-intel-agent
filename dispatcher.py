import os
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

import config

def send_to_telegram(pdf_path: str, caption: str) -> bool:
    """
    Sends the generated PDF summary document to Telegram via Bot API.
    """
    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID

    if not token or not chat_id:
        print("[Dispatcher] ⚠️  Telegram credentials not configured in .env (TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID). Skipping Telegram dispatch.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendDocument"
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"[Dispatcher] ❌ PDF file not found at: {pdf_path}")
        return False

    # Telegram caption limit is 1024 characters
    truncated_caption = caption[:1020]

    try:
        print(f"[Dispatcher] 🚀 Sending PDF to Telegram (Chat ID: {chat_id})...")
        with open(pdf_file, "rb") as f:
            files = {"document": (pdf_file.name, f, "application/pdf")}
            data = {
                "chat_id": chat_id,
                "caption": truncated_caption,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, data=data, files=files, timeout=30)

        if response.status_code == 200:
            print("[Dispatcher] ✅ Successfully delivered PDF report to Telegram!")
            return True
        else:
            print(f"[Dispatcher] ❌ Telegram API error ({response.status_code}): {response.text}")
            return False

    except Exception as e:
        print(f"[Dispatcher] ❌ Failed to send Telegram message: {e}")
        return False


def send_to_email(pdf_path: str, subject: str, html_body: str) -> bool:
    """
    Sends an executive email with the PDF summary attached via SMTP.
    """
    host = config.SMTP_HOST
    port = config.SMTP_PORT
    user = config.SMTP_USER
    password = config.SMTP_PASSWORD
    from_addr = config.EMAIL_FROM
    to_addr = config.EMAIL_TO
    use_ssl = config.SMTP_USE_SSL

    if not user or not password or not to_addr:
        print("[Dispatcher] ⚠️  Email credentials not configured in .env (SMTP_USER / SMTP_PASSWORD / EMAIL_TO). Skipping Email dispatch.")
        return False

    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"[Dispatcher] ❌ PDF file not found at: {pdf_path}")
        return False

    try:
        print(f"[Dispatcher] 🚀 Sending email with PDF attachment to: {to_addr} via {host}:{port}...")

        # Construct multipart email message
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_addr

        # HTML body
        msg_body = MIMEMultipart("alternative")
        html_part = MIMEText(html_body, "html", "utf-8")
        msg_body.attach(html_part)
        msg.attach(msg_body)

        # PDF attachment
        with open(pdf_file, "rb") as f:
            pdf_part = MIMEApplication(f.read(), _subtype="pdf")
            pdf_part.add_header("Content-Disposition", "attachment", filename=pdf_file.name)
            msg.attach(pdf_part)

        # Connect and authenticate
        if use_ssl or port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=25)
        else:
            server = smtplib.SMTP(host, port, timeout=25)
            server.ehlo()
            server.starttls()
            server.ehlo()

        server.login(user, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

        print(f"[Dispatcher] ✅ Successfully sent email with attached PDF to {to_addr}!")
        return True

    except Exception as e:
        print(f"[Dispatcher] ❌ Failed to send email: {e}")
        return False
