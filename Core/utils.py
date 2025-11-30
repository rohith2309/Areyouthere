from passlib.context import CryptContext
import os
from datetime import datetime, UTC,timedelta
from jose import jwt
from typing import Union,Any
from dotenv import load_dotenv

load_dotenv()
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
ACCESS_TOKEN_EXPIRE_MIN=45
REFRESH_TOKEN_EXPIRE_MIN=7*24*60

ALGO=os.getenv("ALGO")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") 
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")


def get_hashed_pwd(rawPwd:str)->str:
    return pwd_context.hash(rawPwd)

def verify_pwd(rawPwd:str,hashPwd:str)->bool:
    return pwd_context.verify(rawPwd,hashPwd)



def create_access_token(subject:Union[str,Any],expires_delta:int=None)->str:
    if expires_delta is not None:
        expires_delta+=datetime.now(UTC)
    else:
        expires_delta=datetime.now(UTC)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    
    to_encode={"exp":expires_delta,"sub":str(subject)}
    encoded_jwt=jwt.encode(to_encode,JWT_SECRET_KEY,ALGO)
    return encoded_jwt


def create_refresh_token(subject:Union[str,Any],expires_delta:int=None)->str:
    if expires_delta is not None:
        expires_delta+=datetime.now(UTC)
    else:
        expires_delta=datetime.now(UTC)+timedelta(minutes=REFRESH_TOKEN_EXPIRE_MIN)
    
    to_encode={"exp":expires_delta,"sub":str(subject)}
    encode_jwt=jwt.encode(to_encode,JWT_REFRESH_SECRET_KEY,ALGO)
    return encode_jwt


                   