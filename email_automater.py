#!/usr/bin/python3
from datetime import date 
import pandas as pd
import parameters as pr
import helper as hh
from connector.data_connector import open_gsheet
from send_email import send_email

if __name__ == "__main__":
    try:
        email_counter = 0
        gheet_df = open_gsheet()
        
        for _, row in gheet_df.iterrows():
            # if payment not paid
            if str(row['paid']).lower() == 'no':
                send_email(
                    subject = f'Dozen Pvt Ltd: Invoice-[{pr.INVOICE_ID}]',
                    receiver_email = row['email'],
                    name = row['person to address'],
                    business_name = row['business name'],
                    invoice_no = pr.INVOICE_ID,
                    invoice_period = hh.convert_invoice_period_format(str(row['invoice period'])),
                    due_date = row['due date'], 
                    amount = row['due amount']
                )
                email_counter += 1
                
        print(f"Total Emails Sent: {email_counter}")

    except Exception as e:
        raise Exception(f"Exception Raised: {e}")