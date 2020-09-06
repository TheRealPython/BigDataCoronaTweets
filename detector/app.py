"""Example Kafka consumer."""

import json
import os
import time
from kafka import KafkaConsumer, KafkaProducer

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Date, String, MetaData, Table, Integer, Numeric, BigInteger)

# Kafka relevant enviroment variables
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
LEGIT_TOPIC = os.environ.get('LEGIT_TOPIC')
FRAUD_TOPIC = os.environ.get('FRAUD_TOPIC')

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
conn.execute('DROP TABLE if EXISTS "BatchLayer"')

class BatchLayer(Base):
    __tablename__ = 'BatchLayer'
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

#Kafka Consumer
consumer = KafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
        auto_offset_reset='latest', enable_auto_commit=True,
        auto_commit_interval_ms=1000, group_id='my-group'
    )

def safe_data_to_db(intervall=60):
    # Safe RAW Data to DB
    timestamp = time.time()
    for message in consumer:
        #print(".")
        transaction = message.value
        #print(transaction)  # DEBUG
        session.add(RAW_BL(id=transaction["id"], date=transaction["created_at"], user_id=transaction["user_id"], location=transaction["location"]))
        session.commit()
        if ( time.time() >= timestamp + intervall):
            break


def compute_data():
    # Big Data Computation
    print("computing ....")
    conn = engine.connect()
    conn.execute('''
        DROP TABLE IF EXISTS "BatchLayer";
        with raw_data as (
        SELECT
            distinct "id","date","user_id", "location"
        FROM
            "RAW_BL"
        ),
        batch_result as (SELECT
            "location",
            count(location) as "count"    
        FROM
            "raw_data"
        group by 
            "location"
        )
        select 
            *
        INTO
            "BatchLayer"
        FROM
            batch_result
        ORDER BY 
            "count"
            DESC;''')
    session.commit()

def excecute_batch_layer(intervall=60):
    # execute data fetch and compute periodic
    while(True):
        safe_data_to_db(intervall)
        compute_data()
        print("sleeping ....")

excecute_batch_layer(10)
# if __name__ == '__main__':
    
#     print("-----------------------------------------------------------------------------")
#     time.sleep(10)
#     for message in consumer:
#         transaction = message.value
#         print(type(transaction))
#         topic = TRANSACTIONS_TOPIC
#         #topic = FRAUD_TOPIC if is_suspicious(transaction) else LEGIT_TOPIC
#         # producer.send(topic, value=transaction)
#         print(topic, transaction)  # DEBUG
#         session.add(BatchLayer(id=transaction["id"], date=transaction["created_at"], user_id=transaction["user_id"], location=transaction["location"]))
#         session.commit()


# psql --host=db --username=postgres --dbname=postgres