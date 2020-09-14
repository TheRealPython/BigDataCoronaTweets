# Setup

## Prerequisites 

Install Docker (https://www.docker.com/)

Install docker-compose (https://docs.docker.com/compose/install/)

## Getting Started
`docker network create kafka-network`


`docker-compose -f docker-compose.kafka.yml up -d`


`docker-compose up --scale web=2 -d`


`docker-compose -f docker-compose-spark.yml up -d`

`./build.sh`

`cd speed/`
`docker build -t bde/spark-app .`
`docker run --network=kafka-network --link spark-master:spark-master -e ENABLE_INIT_DAEMON=false bde/spark-app`

## Using it

Go to *localhost:3000/home*

## Shutdown
`docker-compose -f docker-compose-spark.yml down`

`docker-compose down`

`docker-compose -f docker-compose.kafka.yml down`

`docker network rm kafka-network`

# BigDataCoronaTweets

A project to find locations where Corona is a hot topic based on Tweets, using a BigData-Lambda-Architecure.


# Possible Issues

Incomplete Read Error: https://github.com/tweepy/tweepy/issues/448

by Ruben Härle, Tim Kauer, Jannik Kuom and Sven Metzger