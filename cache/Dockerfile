FROM python:3.6-slim
WORKDIR /srv

ADD ./requirements.txt /srv/requirements.txt

RUN pip install -r requirements.txt

ADD . /srv