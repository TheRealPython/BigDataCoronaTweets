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
from sqlalchemy import (Column, Date, String, MetaData, Table, Integer, Numeric, BigInteger, select)
from sqlalchemy.orm import Query
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import SQLAlchemy
#Redis Cache Server
cache = Cache(config={'CACHE_TYPE': "redis",
                      'CACHE_REDIS_HOST': "redis",
                      'CACHE_REDIS_PORT': 6379
                    })

#Initiate Flask App + Cache
app = Flask(__name__)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
cache.init_app(app)
app.debug=True

#Postgre relevant enviroment variables
user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = 'db'
port = '5432'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db)
db = SQLAlchemy(app)


#Wait for the database to be started
x=False
while (x==False):
    try:
        #DB started
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        ServingLayer_try = Base.classes.ServingLayer
        x = True
    except:
        #DB not started yet
        x=False
        time.sleep(2)
        print("+1")

print("Lets go")

@app.route('/home')
#@cache.cached(timeout=50)  # Cache time einsetzen    
def home(): 

    print("okay")
    conn = db.engine.connect() 
    res = conn.execute('Select * FROM "ServingLayer" LIMIT 30;')
    result = [{column: value for column, value in rowproxy.items()} for rowproxy in res]
    db.session.commit()
    l = result

    return str(l)



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