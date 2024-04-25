import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv

from templates.email_template import get_email_body
import parameters as pr

# Load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir /"configuration" / ".env"
load_dotenv(envars)

sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")

def send_email(subject, receiver_email, name, business_name, invoice_no, invoice_period, due_date, amount):
    # Initializing email message object
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Dozen Pvt.Ltd", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    # msg.set_content()
    msg.add_alternative(
        get_email_body(name, invoice_period, invoice_no, business_name, due_date, amount),
        subtype="html",
    )

    with smtplib.SMTP(pr.EMAIL_SERVER, pr.PORT) as server:  # Application used by mail servers to send and receive emails.
        # Protocol commands
        server.starttls()
        server.login(sender_email, password_email)
        server.send_message(msg)

if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        name="Check Owner",
        business_name="Dozen Pvt. Ltd.",
        invoice_period="Monthly",
        receiver_email="venurajithmal@gmail.com",
        due_date="11 Sep 2023",
        invoice_no="INV-21-12-008",
        amount="5,")
