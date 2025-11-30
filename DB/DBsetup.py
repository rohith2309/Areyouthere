from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
#from Core import settings
import logging
import os
from dotenv import load_dotenv

load_dotenv()

dburl=os.getenv("dburl")
engine=create_engine(dburl)
session=sessionmaker(bind=engine,autoflush=False)

BASE=declarative_base()



def getDb():
    try:
        db=session()
        yield db
    except Exception as e:
        logging.error("db failed to connect",e)    
    finally:
        db.close()    