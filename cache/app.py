import json
import redis
from datetime import datetime
from flask import Flask, request
from flask_caching import Cache
from random import randint

#Redis Cache Server
cache = Cache(config={'CACHE_TYPE': "redis",
                      'CACHE_REDIS_HOST': "redis",
                      'CACHE_REDIS_PORT': 6379
                    })

#Initiate Flask App + Cache
app = Flask(__name__)
cache.init_app(app)

#Render startpage route
@app.route('/')
def one():
    print("yes")
    return ("Hello World")

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