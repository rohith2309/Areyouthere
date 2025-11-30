import smtplib
from dotenv import load_dotenv
import os
import logging

load_dotenv()
from_id=os.getenv("email_id")
password=os.getenv("password")


def configMailer():
    
    try: 
     logging.info(f"Trying to login...... ")
        
     server=smtplib.SMTP_SSL("smtp.gmail.com",465 )
     server.login(from_id,password)
     logging.info(f"logged in...... ") 
     return server
    except Exception as e:
         logging.error(f"failed to login : \n exception: {e}")


         