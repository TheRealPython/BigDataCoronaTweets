FROM bde2020/spark-submit:3.0.0-hadoop3.2
# FROM bde/spark-app-base
COPY template.sh /
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
COPY submit.sh /submit.sh

RUN pip install -r /app/requirements.txt

ENV SPARK_APPLICATION_PYTHON_LOCATION /app/app.py

CMD ["/bin/bash", "/template.sh"]


# docker build -t bde/spark-app .
# docker run --network=kafka-network --link spark-master:spark-master -e ENABLE_INIT_DAEMON=false bde/spark-app
