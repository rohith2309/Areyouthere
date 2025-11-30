from DB.DBsetup import BASE,engine,getDb
from Models.models import Checkin

if __name__=="__main__":
    print("running migrations")
    BASE.metadata.create_all(bind=engine)