import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Date, String, MetaData, Table, Integer, Numeric, BigInteger)

#Postgre relevant enviroment variables
#user = os.environ['POSTGRES_USER']
#pwd = os.environ['POSTGRES_PASSWORD']
#db = os.environ['POSTGRES_DB']
user = 'postgres'
pwd = 'postgres'
db = 'postgres'
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

class BatchLayer(Base):
    __tablename__ = 'ServingLayer'
    location = Column(String, primary_key = True)
    count = Column(Integer)

class RAW_BL(Base):
    __tablename__ = 'RAW_SL'
    id = Column(String, primary_key = True)
    date = Column(Date)
    user_id = Column(String)
    location = Column(String)

conn.execute(""" 
    DROP TABLE IF EXISTS serving_layer_temp; 

    SELECT 
         *
    INTO 
        serving_layer_temp
    FROM 
        batch_layer ;


    UPDATE 
        serving_layer_temp
    SET
        count_id = count_id + speed_layer."count(id)",
        sum_followers_count = sum_followers_count + speed_layer."sum(followers_count)",
        sum_favorite_count = sum_favorite_count + speed_layer."sum(favorite_count)",
        sum_retweet_count = sum_retweet_count + speed_layer."sum(retweet_count)"
    FROM
        speed_layer
    WHERE 
        serving_layer_temp.location = speed_layer.location ;


    INSERT INTO 
        serving_layer_temp
    SELECT 
        * 
    FROM 
        speed_layer
    WHERE 
        speed_layer.location 
    NOT IN (
        SELECT 
            DISTINCT location 
        FROM 
            serving_layer_temp 
    ) ;
    drop table serving_layer ;
    
    alter table serving_layer_temp
    rename to serving_layer ;        
    
""")
session.commit()

print()