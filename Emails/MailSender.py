import os
import smtplib
from email.mime.text import MIMEText
from Emails.MailLayouts import *
from Configuration.config import *

# This function is responsible for sending OTP to users via email
def send_otp_by_mail(recipient:str, user_first_name:str, OTP:int):
    try:
        LOGGER.info(f"Sending OTP via mail to {recipient}")
        # Getting HTML layout for sending OTP
        html_body = otp_mail_layout(user_first_name, OTP)
        # Create MIMEText object with 'html' MIME type
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = f"OTP for registration"
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient
        # Connecting with SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        return True
    except Exception as error:
        LOGGER.error(f"ERROR OCCURED WHILE SEND OTP TO {recipient} :" f"{error}")
        return False
    
    
# This function is responsible for sending a confirmation emails to users 
def registration_success_mail(recipient:str, user_first_name:str):
    try:
        LOGGER.info(f"Sending confirmation e-mail to {recipient}")
        # Getting HTML layout for registration success
        html_body = confirmation_mail_layout(user_first_name)
        # Create MIMEText object with 'html' MIME type
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = f"Registration successfull."
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient
        # Connecting with SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        return True
    except Exception as error:
        LOGGER.error(f"ERROR OCCURED WHILE SEND OTP TO {recipient} :" f"{error}")
        return False    