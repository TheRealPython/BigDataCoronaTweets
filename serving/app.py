import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Date, String, MetaData, Table, Integer, Numeric, BigInteger)

#Postgre relevant enviroment variables
user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = 'db'
port = '5432'

time.sleep(20)
print("starting BL ....")

#engine creation for postgres connection
engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db)) 
Base = declarative_base()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

conn = engine.connect()

class ServingLayer(Base):
    __tablename__ = 'ServingLayer'
    location = Column(String, primary_key = True)
    count = Column(Integer)

class RAW_BL(Base):
    __tablename__ = 'RAW_BL'
    id = Column(String, primary_key = True)
    date = Column(Date)
    user_id = Column(String)
    location = Column(String)

Base.metadata.create_all(engine) 
metadata = MetaData()  


conn.execute('''
    DROP TABLE IF EXISTS "ServingLayer"; 

    SELECT 
         *
    INTO 
        "ServingLayer"
    FROM 
        "BatchLayer" ;
 ''')

session.commit()

print(1234)