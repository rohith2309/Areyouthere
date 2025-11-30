import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends,HTTPException,Request,FastAPI,status
from Models.models import Token
import os
from dotenv import load_dotenv

load_dotenv()


ACCESS_TOKEN_EXPIRE_MIN=45
REFRESH_TOKEN_EXPIRE_MIN=7*24*60

ALGO=os.getenv("ALGO")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") 
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
def decodeJwt(jwtToken:str)->str:
    try:
        payload=jwt.decode(jwtToken,JWT_SECRET_KEY,ALGO)
        
        return payload
    except InvalidTokenError:
        return None

class JWTBearer(HTTPBearer):
    
    def __init__(self,auto_error:bool=True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> dict:
        creds: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if not creds:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code"
            )
        
        if creds.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme"
            )
        
        payload = self.verify_token(creds.credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token or expired token"
            )
        
        
        return payload
    
    
    def verify_token(self,tkn:str):
        isToken:bool=False
        try:
         payload=decodeJwt(tkn)
        except:
            payload=None 
        
        if payload:
            isToken=True
        
        return isToken     
    
jwt_bearer = JWTBearer()       
             
                 