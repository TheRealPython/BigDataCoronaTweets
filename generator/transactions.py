"""Utilities to model money transactions."""

# from random import choices, randint
# from string import ascii_letters, digits

# account_chars: str = digits + ascii_letters
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
print("Wait on rate limit")
api = tweepy.API(auth) 
print("Hurray")
def get_twitter_data():
    try:
        res = api.search("Corona")
        print(res)
        for i in res:
            #time.sleep(2)
            record = ''
            record += str(i.user.id_str)
            record += ';'
           
            record += str(i.user.location)
            record += ';'
            record += str(i.favorite_count)
            record += ';'
            # record += str(i.retweet_count)
            # record += ';'
             # record += str(i.user.followers_count)
            # record += ';'
            print(record)
        return (record)
    except:
        return (12)
        #producer.send(topic_name, str.encode(record))
        # producer.send(topic_name, value=record)

# print("works")

# producer = KafkaProducer(
#     bootstrap_servers=['kafka:9092'],
#     value_serializer=lambda x: dumps(x).encode('utf-8')
# )
# topic_name = 'tweets-lambda1'

# print("yes")

# def periodic_work(interval):
#     while True:
#         get_twitter_data()
#         #interval should be an integer, the number of seconds to wait
#         time.sleep(interval)
        

# periodic_work(60 * 0.1)  # get data every couple of minutes



# def _random_account_id() -> str:
#     """Return a random account number made of 12 characters."""
#     return ''.join(choices(account_chars, k=12))


# def _random_amount() -> float:
#     """Return a random amount between 1.00 and 1000.00."""
#     return randint(100, 100000) / 100


# def create_random_transaction() -> dict:
#     """Create a fake, randomised transaction."""
#     return {
#         'source': _random_account_id(),
#         'target': _random_account_id(),
#         'amount': _random_amount(),
#         # Keep it simple: it's all euros
#         'currency': 'EUR',
#     }
