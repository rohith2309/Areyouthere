import uuid
from DB.DBsetup import BASE
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime,UUID
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

from sqlalchemy.sql import func

class User(BASE):
    __tablename__="User"
    
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name=Column(String,nullable=False)
    email = Column(String, unique=True, index=True)
    password=Column(String,nullable=False)
    
    verified_acc=Column(Boolean,default=False)
    
    seniors = relationship("Senior", back_populates="user")
    checkins=relationship("Checkin",back_populates="user")

class Token(BASE):
    __tablename__="Token"
    
    user_id=Column(UUID(as_uuid=True), ForeignKey("User.id"))
    access_token=Column(String(500),primary_key=True)
    refresh_token=Column(String(500),nullable=False)
    created_time=Column(DateTime,default=lambda: datetime.now(timezone.utc))
    status = Column(Boolean)

class Senior(BASE):
    
    __tablename__="Senior"
    
    id =Column(Integer,primary_key=True,autoincrement=True)
    seniorName=Column(String,nullable=False)
    seniorEmail=Column(String,nullable=False)
    buddy1=Column(String,nullable=False)
    buddy1Email=Column(String,nullable=False)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("User.id"))
    
    user = relationship("User", back_populates="seniors")
    checkins = relationship("Checkin", back_populates="senior")
    


class Checkin(BASE):
    __tablename__ = "Checkin"

    id = Column(Integer, primary_key=True, autoincrement=True)


    senior_id = Column(Integer, ForeignKey("Senior.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("User.id"))

    
    senior_checked = Column(Boolean, default=False)
    buddy_checked = Column(Boolean, default=False)
    buddy_notified=Column(Boolean,default=False)
    user_notified = Column(Boolean, default=False)
    buddy_email=Column(String,nullable=False)


    
    notification_sent = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    senior_acked_time = Column(DateTime(timezone=True), default=None )
    buddy_acked_time = Column(DateTime(timezone=True), default=None)
    
    user=relationship("User",back_populates="checkins")
    senior = relationship("Senior", back_populates="checkins")
    
    
          