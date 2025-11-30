from fastapi import FastAPI,Depends
from Controller.Api.v1 import user
from config.MailConfig import configMailer
from DB.DBsetup import BASE,engine,getDb

import logging

from Models.models import Checkin

from sqlalchemy.orm import Session

from datetime import datetime,UTC,timezone
from fastapi.responses import HTMLResponse

from apscheduler.schedulers.background import BackgroundScheduler
from Jobs.StatusJobs import CheckinEntry,SendUserStatus,CheckinStatus

BASE.metadata.create_all(bind=engine)

scheduler=BackgroundScheduler()
scheduler.add_job(CheckinEntry,'cron',hour=00, minute=00)
scheduler.add_job(CheckinStatus,'cron',hour=00,minute=1)
scheduler.add_job(SendUserStatus,'cron',hour=00,minute=2)



app = FastAPI()

@app.get("/")
async def home():
   
    return {"message": "Hello world"}

@app.on_event("startup")
async def startup():
    logging.info("initiate startup")
    scheduler.start()
    
    BASE.metadata.create_all(bind=engine)
    logging.info("end startup")


#testing receive ack

@app.get("/acknowledge")
async def acknowledge(user_id: int, request_id: int, db: Session = Depends(getDb)):
    
    try:
        chechinRec=db.query(Checkin).filter(Checkin.id==request_id).first()
        chechinRec.senior_checked=True
        chechinRec.senior_acked_time=datetime.now(timezone.utc)
        db.commit()
        db.refresh(chechinRec)
        return HTMLResponse(content=
            """
            <html>
            <bodystyle="font-family:Arial; text-align:center; padding:50px;">
             <div>
             <H1>Thank you for Acknowledging, have a good day!</H1>
             </div>
            </body>
            </html>
            
            """
            
            ,status_code=200)
    except Exception as e:
        logging.error(e)
   
    finally:
        db.close()        
    
@app.get('/acknowledge-buddy')
async def buddyAcknowledge(senior_id:int,request_id:int,db:Session=Depends(getDb)):
      
      try:
        chechinRec=db.query(Checkin).filter(Checkin.id==request_id).first()
        chechinRec.buddy_checked=True
        chechinRec.buddy_acked_time=datetime.now(UTC)
        db.commit()
        db.refresh(chechinRec)
        return HTMLResponse(content="""
            <html>
            <bodystyle="font-family:Arial; text-align:center; padding:50px;">
             <div>
             <H1>Thank you for Acknowledging, have a good day!</H1>
             </div>
            </body>
            </html>
            
            """,status_code=200)
      except Exception as e:
          logging.log(e)
      finally:
          db.close     
    
        

app.include_router(user.userRoutes,prefix="/Api/v1",tags=['user'])


