from pydantic import BaseModel, EmailStr,UUID4
from datetime import datetime
from typing import Optional, List




class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password:str   

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserResponse(UserBase):
    id: UUID4

    class Config:
        from_attributes = True  

class TokenScheme(BaseModel):
    access_token: str
    refresh_token:str
    class Config:
        from_attributes = True 

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime    


class SeniorBase(BaseModel):
    seniorName: str
    seniorEmail: EmailStr
    buddy1: str
    buddy1Email: EmailStr


class SeniorCreate(SeniorBase):
    user_id: int


class SeniorResponse(SeniorBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True




class CheckinBase(BaseModel):
    senior_checked: bool = False
    buddy_checked: bool = False
    user_notified: bool = False
    notification_sent: Optional[datetime] = None
    senior_acked_time: Optional[datetime] = None
    buddy_acked_time: Optional[datetime] = None


class CheckinCreate(CheckinBase):
    user_id: int
    senior_id: int


class CheckinResponse(CheckinBase):
    id: int
    user_id: int
    senior_id: int

    class Config:
        from_attributes = True
