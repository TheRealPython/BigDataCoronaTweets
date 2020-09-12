FROM python:3.7-alpine
WORKDIR /srv

ADD ./requirements.txt /srv/requirements.txt

RUN pip install -r requirements.txt

ADD . /srv