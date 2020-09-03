import tweepy
import time
from json import dumps
from kafka import KafkaConsumer, KafkaProducer

consumer_key = "wlERBY63NRgX28lZB5Lo1lqHe"
consumer_secret = "68IbgR2k5HnPzjbrN7wh2EIAuvvExpDjr1IJl2L2Z7myhkA26t"
access_token = "1300058448432955393-vtCd4lMpMfJnfxcvC7hCUGQKaqrymm"
access_token_secret = "gemqcDjUQWIfzWOBDDQQNsdqJ1WEfP0FSU3IGZw90ZBAv"

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object by passing in auth information
api = tweepy.API(auth) 

def get_twitter_data():
    print("Requested Data...")
    res = api.search("Corona")
    #print(res)
    for i in res:
        #time.sleep(5)
        record = ''
        record += str(i.user.id_str)
        record += ';'
        record += str(i.user.followers_count)
        record += ';'
        record += str(i.user.location)
        record += ';'
        record += str(i.favorite_count)
        record += ';'
        record += str(i.retweet_count)
        record += ';'
        #print(record)
        print("sending...")
        #producer.send(topic_name, str.encode(record))
        producer.send(topic_name, value=record)

print("works")

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)
topic_name = 'tweetLambda1'

print("yes")

def periodic_work(interval):
    while True:
        get_twitter_data()
        #interval should be an integer, the number of seconds to wait
        time.sleep(interval)
        

periodic_work(60 * 0.1)  # get data every couple of minutes


#get_twitter_data()

####
#get started

# docker-compose -f docker-compose-expose.yml up

#docker-compose stop

#python twitter_data.py

#python consumer.py

