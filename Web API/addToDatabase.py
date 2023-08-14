import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from content.DataBase import alchemy

# Connect to the database
engine = create_engine('sqlite:///../content/DataBase/mydatabase.db')
Session = sessionmaker(bind=engine)
session = Session()

def add_user(email, id):
    new_user = alchemy.User(email=email, id=id)
    session.add(new_user)
    session.commit()

def add_upload(filename, status, user, uid):
    id = random.Random().randint(0, 1000000000)
    new_upload = alchemy.Upload(filename=filename, status=status, id = id, user = user, uid = uid)
    session.add(new_upload)
    session.commit()

def find_user(email):
    user = session.query(alchemy.User).filter_by(email=email).first()
    return user

def find_upload(uid):
    upload = session.query(alchemy.Upload).filter_by(uid=uid).first()
    return upload

def update_upload_status(upload, status):
    upload.status = status
    session.commit()
