import json
import smtplib
import pandas as pd
from datetime import datetime
from typing import Tuple
from email.message import EmailMessage
from email.utils import formataddr

PORT = 587
EMAIL_SERVER = "smtp.gmail.com"
GSHEET_CREDS_PATH = ''
SPREADSHEET_NAME = ''
SPREADSHEET_URL = ''
WORKSHEET_NAME = ''
sender_email = ''
password_email = ''

def get_email_body(name:str, invoice_period:str, invoice_no:str, business_name:str, due_date:str, amount:str):
    return f"""\
        <html>
            <body>
                <p>Hi {name},</p>
                <p>Friendly reminder of the payment of <strong>{invoice_period}</strong> (Invoice No. {invoice_no}) for {business_name} is due on <strong>{due_date}</strong>.</p>
                <p>Please confirm your payment of <strong>LKR {amount}</strong>.</p>
                <p>Best regards,<br>Dozen Solutions Pvt Ltd</p>
            </body>
        </html>
        """

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

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:  # Application used by mail servers to send and receive emails.
        # Protocol commands
        server.starttls()
        server.login(sender_email, password_email)
        server.send_message(msg)



def open_gsheet() -> pd.DataFrame:
    data = [{
        "email":"venurajithmal@gmail.com",
        "personToAddress":"Venura Pussella",
        "businessName":"Higgins & Sons",
        "invoicePeriod":"2024-02",
        "dueDate":"2024-04-27",
        "dueAmount":"50000",
        "paid":"no"
        }]
 
    df = pd.DataFrame.from_dict(data)

    return df

def convert_invoice_period_format(invoice_period_input_str:str):
    input_date = datetime.strptime(invoice_period_input_str, '%Y-%m') # Convert string to datetime object
    return input_date.strftime('%B, %Y') # Format the datetime object

def generate_invoice_id() -> str:
    return 'DZN-10120'

def send_invoice_reminder_mails() -> Tuple[int, list]:
    email_counter = 0
    gheet_df = open_gsheet()
    
    mail_sent_clients = []

    for _, row in gheet_df.iterrows():
        # if payment not paid
        if str(row['paid']).lower() == 'no':
            invoice_id = generate_invoice_id()
            send_email(
                subject = f'Dozen Pvt Ltd: Invoice-[{invoice_id}]',
                receiver_email = row['email'],
                name = row['personToAddress'],
                business_name = row['businessName'],
                invoice_no = invoice_id,
                invoice_period = convert_invoice_period_format(str(row['invoicePeriod'])),
                due_date = row['dueDate'], 
                amount = row['dueAmount']
            )
            mail_sent_clients.append(str(row['businessName']))
            email_counter += 1
            
    print(f"Total Emails Sent: {email_counter}")
    return email_counter, mail_sent_clients

def lambda_handler(event, context):
    # TODO implement
    email_count, mail_sent_clients = send_invoice_reminder_mails()

    return {
        'statusCode': 200,
        'body': json.dumps({
            "message" : "Successfully completed the Daily Invoice reminder job.",
            "emails_sent" : f"{email_count}",
            "mail_sent_clients" : ', '.join(mail_sent_clients)
            })
    }
