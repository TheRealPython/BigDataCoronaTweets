import json
import redis
from datetime import datetime
from flask import Flask, request
from flask_caching import Cache
from random import randint

import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Date, String, MetaData, Table, Integer, Numeric, BigInteger)
from sqlalchemy.orm import Query
#Redis Cache Server
cache = Cache(config={'CACHE_TYPE': "redis",
                      'CACHE_REDIS_HOST': "redis",
                      'CACHE_REDIS_PORT': 6379
                    })

#Initiate Flask App + Cache
app = Flask(__name__)
#cache.init_app(app)

#Postgre relevant enviroment variables
user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = 'db'
port = '5432'


#engine creation for postgres connection
engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db)) 
Base = declarative_base()
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Session.configure(bind=engine)
session = Session()

conn = engine.connect()

class BatchLayer(Base):
    __tablename__ = 'BatchLayer'
    location = Column(String, primary_key = True)
    count = Column(Integer)

class ServingLayer(Base):
    __tablename__ = 'ServingLayer'
    location = Column(String, primary_key = True)
    count = Column(Integer)

Base.metadata.create_all(engine)
metadata = MetaData()

#Render startpage route
# @app.route('/')
# #@cache.cached(timeout=50)  # Cache time einsetzen    
# def one():
#     print("yes")            # @Jannik: hier muss der DB-Abruf rein
#     return ("Hello World")


@app.route('/home')
#@cache.cached(timeout=50)  # Cache time einsetzen    
def home(): 
    #some_profile = session.query(Profile).filter(Profile.id == req).first()
    #x = session.query(ServingLayer.location, ServingLayer.count).orderby(ServingLayer.count.desc()).limit(10).all() 
    result = session.query(BatchLayer).all()
    y=0
    lana = []
    for row in result:
        if y < 5:
            print ("Name: ",row.location, "Address:",row.count)
            y=y+1
            lana.append(row.location)
            lana.append(row.count)
        else:
            break
    return str(lana)


####################################################################
#Cache Server Test Routes#
##########################

#cached
@app.route('/nice')
@cache.cached(timeout=50)
def index():
    return 'Cached for 50s'

#not cached
@app.route('/random')
#@cache.cached(timeout=50)
def randomizerr():
    randumnum = randint(1, 6000)
    return f'A random number {randumnum}'

#cached
@app.route('/cache')
@cache.cached(timeout=10)
def cacherr():
    randumnum = randint(1, 6000)
    return f'A random number being cached for 10 secs: {randumnum}'

#cached with function
@app.route('/cache2')
@cache.cached(timeout=10)
def cacherr2():
    randumnum = calculate()
    return f'A random number being cached for 10 secs: {randumnum}'

def calculate():
    num = randint(1, 6000)
    return num