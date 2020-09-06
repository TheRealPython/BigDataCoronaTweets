"""Example Kafka consumer."""

import json
import os

from kafka import KafkaConsumer, KafkaProducer

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import (Column, Date, String, MetaData, Table)

# Kafka relevant enviroment variables
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
LEGIT_TOPIC = os.environ.get('LEGIT_TOPIC')
FRAUD_TOPIC = os.environ.get('FRAUD_TOPIC')

# Postgre relevant enviroment variables
# user = os.environ['POSTGRES_USER']
# pwd = os.environ['POSTGRES_PASSWORD']
# db = os.environ['POSTGRES_DB']
# host = 'db'
# port = '5432'

# engine creation for postgres connection
# engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db)) 
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()

# class Batch(Base):
#     __tablename__ = 'BatchLayer'
#     date = Column(Date)
    

if __name__ == '__main__':
    consumer = KafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
    )
    for message in consumer:
        transaction = message.value
        topic = TRANSACTIONS_TOPIC
        #topic = FRAUD_TOPIC if is_suspicious(transaction) else LEGIT_TOPIC
        # producer.send(topic, value=transaction)
        print(topic, transaction)  # DEBUG
