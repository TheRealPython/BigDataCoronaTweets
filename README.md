# BigDataCoronaTweets

A project to find locations where Corona is a hot topic based on Tweets, using a BigData-Lambda-Architecure.

## Prerequisites 

Install Docker (https://www.docker.com/)

Install docker-compose (https://docs.docker.com/compose/install/)

## Getting started 

 `docker network create kafka-network`
  
  
  `docker-compose -f docker-compose.kafka.yml up -d`
  
  
  `docker-compose up -d`

Shut down

 `docker-compose down`
 
 `docker-compose -f docker-compose.kafka.yml`

 `docker network rm kafka-network`



---------------------------------------------------------------

deprecated

Lambda Architecture handling latest Tweets about Corona


  get started

  `docker-compose -f docker-compose-expose.yml up`
  
  `python twitter_data.py`

  `python consumer.py`


  `docker-compose stop`
  
  
---------------------------------------------
# useful links:

https://github.com/juggernaut/nginx-flask-postgres-docker-compose-example

by Ruben Härle, Tim Kauer, Jannik Kuom and Sven Metzger
