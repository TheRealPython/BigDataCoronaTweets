import os
import flask
import sqlalchemy
from faker import Faker
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from sqlalchemy import (
    BIGINT, BigInteger, Column, Date, Float, ForeignKey, ForeignKeyConstraint,
    Integer, MetaData, String, Table, alias, and_, create_engine, exists,
    insert, inspect, or_, select, update)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (Query, aliased, load_only, relationship, sessionmaker)
from wtforms import (DateField, FloatField, HiddenField, IntegerField, StringField, SubmitField)

app = Flask(__name__)

#function for datetime
fake = Faker()

#Postgre relevant enviroment variables
user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = 'db'
port = '5432'

#connection to postgresql database
engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db))
Base = declarative_base()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


#Route for the home page where the links to the other pages are shown
@app.route('/home')
def home():
    return render_template("Home.html")

#Form of the Batch Layer
class RAW_BL(FlaskForm):
    id = StringField("RAW_BL_ID")
    date = DateField("RAW_BL_date")
    user_id = StringField("RAW_BL_user_id")
    location = StringField("RAW_BL_location")

#starting the flask app
if __name__ == '__main__':
    app.run(debug = True)