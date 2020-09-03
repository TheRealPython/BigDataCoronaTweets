FROM python:3.6-alpine
ADD . /
WORKDIR /

RUN pip install kafka-python

CMD ["python","./consumer.py"]