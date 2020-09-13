# BigDataCoronaTweets

A project to find locations where Corona is a hot topic based on Tweets, using a BigData-Lambda-Architecure.

## Prerequisites 

Install Docker (https://www.docker.com/)

Install docker-compose (https://docs.docker.com/compose/install/)

## Getting started 

 `docker network create kafka-network`
  
  
  `docker-compose -f docker-compose.kafka.yml up -d`
  
  
  `docker-compose up -d`
  
Open a browser window
`http://localhost:8000/`

Shut down

 `docker-compose down`
 
 `docker-compose -f docker-compose.kafka.yml down`

 `docker network rm kafka-network`


  
  
---------------------------------------------
# useful links:

https://github.com/juggernaut/nginx-flask-postgres-docker-compose-example

# Possible Issues

Incomplete Read Error: https://github.com/tweepy/tweepy/issues/448

by Ruben Härle, Tim Kauer, Jannik Kuom and Sven Metzger
