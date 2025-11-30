import smtplib
from dotenv import load_dotenv
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

load_dotenv()
from_id=os.getenv("email_id")
password=os.getenv("password")


def get_html_template(url: str ) -> str:
   
    

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .button {{
                background-color: #4CAF50; 
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <h2>Action Required</h2>
        <p>Please acknowledge receipt of this important message by clicking the button below.</p>
        <a href={url} class="button">Acknowledge Receipt</a>
        <p>If you cannot click the button, please copy and paste this link into your browser:</p>
        <p>{url}</p>
    </body>
    </html>
    """
    return html_content


def get_user_notify_temp(name:str,status:str):
    
    html=f"""
    
    <!doctype>
    <HTML>
     <head>
      <style>
      
      </style>
     </head>
     
     <body>
     
     <p>Hi {name},</p>
     <p>today's report is attached below please have look.</p>
     
     <h4>{status}</h4>
     
     
     <h5>Thank you,</h5>
     <h6>AreYouThere team</h6>
     
     
     
     
     </body>
     
     
     
    </HTML>
    
    
    """
    return html


        
def send_acknowledgment_email(to_email: str, user_id: int, request_id: str,server):
    path="acknowledge"
    acknowledgment_url = f"http://127.0.0.1:8000/{path}?user_id={user_id}&request_id={request_id}"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Action Required: Please Acknowledge"
    msg["From"] = from_id
    msg["To"] = to_email

 
    text = f"""
    Action Required
    Please acknowledge receipt of this message by visiting the following link:
    {acknowledgment_url}
    """

    
    html = get_html_template(url=acknowledgment_url)

   
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)

   
    try:
            server.sendmail(from_id, to_email, msg.as_string())
            print(f"Email successfully sent to {to_email}")
    except Exception as e:
        logging.error("error in  ack {e}")
        

def send_buddy_acknowledgment_email(to_email: str, senior_id: int, request_id: str,server):
    
    #Must change later on from Local Host
    buddy_url=f"http://127.0.0.1:8000/acknowledge-buddy?senior_id={senior_id}&request_id={request_id}"
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Action Required: Please Acknowledge"
    msg["From"] = from_id
    msg["To"] = to_email

 
    text = f"""
    Action Required
    Please acknowledge receipt of this message by visiting the following link:
    {buddy_url}
    """

    
    html = get_html_template(url=buddy_url)

   
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)

   
    try:
            server.sendmail(from_id, to_email, msg.as_string())
            print(f"Email successfully sent to {to_email}")
    except Exception as e:
        logging.error("error in buddy ack {e}")
        
        

def UserNotification(toEmail:str,username:str,status:str,server):
    msg=MIMEMultipart("alternative")
    msg["From"] = from_id
    msg["To"] = toEmail
    msg["Subject"]=f"Checkin Status - {datetime.today()}" 
    
    
    html=get_user_notify_temp(username,status) 
    
    part1=MIMEText(html,"html")
    msg.attach(part1)
    
    try:
        
        server.sendmail(from_id,toEmail,msg.as_string())
    except Exception as e:
        logging.error("error in user notification {e}")
             
    
         