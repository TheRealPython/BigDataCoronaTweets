#ARG ubuntu_version=18.04
#FROM ubuntu:${ubuntu_version}
#Use ubuntu 18:04 as your base image
FROM ubuntu:18.04
#Any label to recognise this image.
LABEL image=Spark-base-image
ENV SPARK_VERSION=2.4.1
ENV HADOOP_VERSION=2.7
#Run the following commands on my Linux machine
#install the below packages on the ubuntu image
RUN apt-get update -qq && \
    apt-get install -qq -y gnupg2 wget openjdk-8-jdk scala
#Download the Spark binaries from the repo
WORKDIR /
RUN wget --no-verbose http://apache.mirror.iphh.net/spark/spark-3.0.1/spark-3.0.1-bin-hadoop2.7.tgz && ls
#RUN file /spark-3.0.1-bin-hadoop2.7.tgz
# Untar the downloaded binaries , move them the folder name spark and add the spark bin on my class path
RUN tar -zxvf /spark-3.0.1-bin-hadoop2.7.tgz && \
    mv spark-3.0.1-bin-hadoop2.7 spark && \
    echo "export PATH=$PATH:/spark/bin" >> ~/.bashrc
#Expose the UI Port 4040
EXPOSE 4040



FROM spark-base-image
WORKDIR /usr/app

# RUN apt-get update
# RUN apt-get install default-jdk -y
RUN apt install -qq -y python3-pip
ADD ./requirements.txt ./
RUN pip3 install -r requirements.txt
ADD ./ ./
RUN cd /spark && ./bin/spark-submit /usr/app/app.py --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 















# From spark-kafka
# # FROM python:3.6-stretch

# WORKDIR /usr/app

# # RUN apt-get update
# # RUN apt-get install default-jdk -y

# ADD ./requirements.txt ./
# RUN pip install -r requirements.txt
# ADD ./ ./


