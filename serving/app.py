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
print("starting SpL ....")

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

Base.metadata.create_all(engine)
metadata = MetaData()

def check_connection():
    try:
        # try to join tables for frontend
        print("yayy")
        conn.execute('''
            BEGIN;
            DROP TABLE IF EXISTS "ServingLayer";
            with batch_result2 as (SELECT
            "location", SUM("count") "count"
            FROM
            (
            SELECT "location", "count"
            FROM "BatchLayer"
            UNION ALL
            SELECT "location", "count"
            FROM "speedlayer"
            ) t
            GROUP BY "location")
            select *
            INTO
            "ServingLayer"
            FROM
            batch_result2
            ORDER BY
            "count"
            DESC;
            COMMIT; ''')
        session.commit()
    except:
        print('Test')

while True:
    print("Start loop to merge data...")
    check_connection()
    time.sleep(30)
    print("Data merged")

print("Code in Serving Layer exited")
print(1234)
