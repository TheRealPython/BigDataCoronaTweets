
import tweepy
import json
from kafka import KafkaProducer
from tweepy import Stream
from tweepy.streaming import StreamListener

import os
from time import sleep

#Twitter API Credentials
consumer_key = "wlERBY63NRgX28lZB5Lo1lqHe"
consumer_secret = "68IbgR2k5HnPzjbrN7wh2EIAuvvExpDjr1IJl2L2Z7myhkA26t"
access_token = "1300058448432955393-vtCd4lMpMfJnfxcvC7hCUGQKaqrymm"
access_token_secret = "gemqcDjUQWIfzWOBDDQQNsdqJ1WEfP0FSU3IGZw90ZBAv"

#Kafka Variables
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object by passing in auth information
print("Wait on rate limit")
api = tweepy.API(auth) 

class MyListener(StreamListener):
 
    def on_data(self, data):
        producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
        )
        
        try:
            # try sending data to topic
            tweets = json.loads(data)
            tweet_data = {"id" : tweets["id"], "created_at": tweets["created_at"], "user_id" : tweets["user"]["id"], "location" : tweets["user"]["location"]}
            producer.send(TRANSACTIONS_TOPIC, value=tweet_data)
            return tweet_data
            
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

# executing Stream
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['Corona', "Covid-19"])






