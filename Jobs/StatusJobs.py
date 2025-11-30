
from DB.DBsetup import getDb
from datetime import datetime,timedelta,UTC,timezone
from Models.models import Checkin,Senior
from config.MailConfig import configMailer
import logging
from Service.mailingService.mailer import get_html_template,send_acknowledgment_email,send_buddy_acknowledgment_email,UserNotification

mailServer=configMailer()


def CheckinEntry():
    db_gen=getDb()
    db = next(db_gen)
    
    try:
        seniors=db.query(Senior).all()
        print(seniors)
        for senior in seniors:
            checkin=Checkin(
              senior_id=senior.id,
              user_id=senior.user_id,
              buddy_email=senior.buddy1Email  
            )
            db.add(checkin)
            db.commit()
            
            
            send_acknowledgment_email(senior.seniorEmail,senior.id,checkin.id,mailServer)
            
            
        
    except Exception as e:
        logging.error(f"CheckinEntry DB {e}")
        db.rollback()
    finally:
        db.close()    
        
    
def CheckinStatus():
    dbgen=getDb()
    db=next(dbgen)
    today=datetime.now(UTC).date()
    tomorrow= today+timedelta(days=1)
    
    try:
        checkin=db.query(Checkin).filter(Checkin.senior_checked==False,Checkin.notification_sent>=today,Checkin.notification_sent<tomorrow).all()
        if checkin:
         print("filltered today'checkin")
        
        for checkinRec in checkin:
            checkinRec.buddy_notified=True
            db.commit()
            send_buddy_acknowledgment_email(checkinRec.buddy_email,checkinRec.senior_id,checkinRec.id,mailServer)
    except Exception as e:
        logging.error(f"CheckinEntry DB {e}")
        db.rollback()
    finally:
        db.close()        



def SendUserStatus():
    dbgen=getDb()
    db=next(dbgen)
    today = datetime.now(timezone.utc)
    start=datetime(today.year,today.month,today.day,tzinfo=timezone.utc)

    tomorrow= start+timedelta(days=1)
    
    print(f"today {start}")
    print(f"tomo {tomorrow}")
    try:
        checkin=db.query(Checkin).filter(Checkin.user_notified==False,Checkin.notification_sent>=start,Checkin.notification_sent<tomorrow).all()
        print(checkin)
        for checkinRec in checkin:
            checkinRec.user_notified=True
            db.commit()
            UserNotification(checkinRec.user.email,checkinRec.user.name,checkinRec.senior_checked,mailServer)
        
    
    
    except Exception as e:
        logging.error(f"CheckinEntry DB {e}")
        db.rollback()
         
    
    finally:
         db.close()        

#CheckinEntry()
#CheckinStatus()           
#SendUserStatus()   