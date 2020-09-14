FROM bde2020/spark-submit:3.0.0-hadoop3.2

COPY template.sh /
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
COPY submit.sh /submit.sh

RUN pip install -r /app/requirements.txt

ENV SPARK_APPLICATION_PYTHON_LOCATION /app/app.py

CMD ["/bin/bash", "/template.sh"]