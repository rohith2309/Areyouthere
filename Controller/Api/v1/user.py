from fastapi import APIRouter, Depends, status,HTTPException
from Models.models import User,Senior,Token
from Schema.userSchema import UserCreate, UserResponse,SeniorResponse,SeniorCreate,UserLogin,TokenScheme
from DB.DBsetup import getDb
from sqlalchemy.orm import Session

import logging
from Core.utils import get_hashed_pwd,verify_pwd,create_access_token,create_refresh_token
from Core.auth_bearer import JWTBearer

userRoutes=APIRouter()
@userRoutes.post("/user/register",response_model=UserResponse)
async def createUser(user:UserCreate, db:Session = Depends(getDb)):
    
    try:
        uemail=db.query(User).filter(User.email==user.email).first()
        if uemail:
           raise HTTPException(status_code=status.HTTP_302_FOUND, detail="User already exist")
        encrypt_pwd=get_hashed_pwd(user.password)
        _nUser=User(name=user.name,email=user.email,password=encrypt_pwd)
        db.add(_nUser)
        db.commit()
        db.refresh(_nUser)
        db.close()
        return _nUser
     
    except Exception as e:
       
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")
        
@userRoutes.post("/user/login",response_model=TokenScheme)
async def LoginUser(user:UserLogin,db:Session=Depends(getDb)):
    try:
        uemail= db.query(User).filter(User.email==user.email).first()
        if uemail is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="incorrect email id")
        
        if not verify_pwd(user.password,uemail.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect password")
        
        access=create_access_token(uemail.id)
        refresh=create_refresh_token(uemail.id)
        
        token=Token(user_id=uemail.id,access_token=access,refresh_token=refresh,status=True)
        db.add(token)
        db.commit()
        db.refresh(token)
        return token
    except Exception as e:
        logging.error(f"error {e}")
        
        
                

@userRoutes.get("/user/secure")
async def secureTest(dependencies=Depends(JWTBearer())):
   
    return {"message": "THIS IS A SECURE PAGE"}

@userRoutes.post("/senior/register",response_model=SeniorResponse)
async def RegisterSenior(senior:SeniorCreate,db:Session=Depends(getDb)):
    _msenior=Senior(seniorName=senior.seniorName,seniorEmail=senior.seniorEmail,buddy1=senior.buddy1,buddy1Email=senior.buddy1Email,user_id=senior.user_id)
    
    db.add(_msenior)
    db.commit()
    db.refresh(_msenior)
    return _msenior
    
    

    