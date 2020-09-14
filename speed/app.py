from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import translate
from pyspark.sql.functions import current_date
from pyspark.sql import Row
from pyspark.sql.functions import expr 
import time
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *

#starting Spark Session
spark = SparkSession \
    .builder \
    .appName("bigdatacoronatweets_broker_1") \
    .config("spark.sql.shuffle.partitions","2") \
    .getOrCreate()


# Create DataFrame representing the stream of input lines from connection to localhost:9092
data_stream_Raw = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "broker:9092") \
  .option("subscribe", "queueing.transactions") \
  .option("startingOffsets","earliest") \
  .load() \

tweet = Row("id", "created_at", "user_id", "location")

# StructType for encoding JSON from Kafka Stream
struct = StructType([
    StructField("id", StringType()),
    StructField("created_at", StringType()),
    StructField("user_id", StringType()),
    StructField("location", StringType()),
])

# Computation
data_stream = data_stream_Raw.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

data_stream_Parsed = data_stream.select(from_json("value", struct).alias("message"))

messageFlattenedDF = data_stream_Parsed.selectExpr("message.id", "message.created_at", "message.user_id", "message.location")

df = messageFlattenedDF.groupBy("location").count()

query = df.writeStream \
    .format("memory") \
    .queryName("SpeedLayer") \
    .trigger(processingTime='60 seconds') \
    .outputMode("complete") \
    .start()


def exportToPostgres():
    # writing Data to postgres database
    df = spark.sql("select * from SpeedLayer")

    mode = "overwrite"
    url = "jdbc:postgresql://db:5432/postgres"
    properties = {"user": "postgres","password": "postgres","driver": "org.postgresql.Driver"}
    df.write.jdbc(url=url, table="speedlayer", mode=mode, properties=properties)

while True:
    exportToPostgres()
    time.sleep(10)
