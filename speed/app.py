from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import translate
from pyspark.sql import Row
from pyspark.sql.functions import expr 
import time
from pyspark.sql.functions import from_json, col

spark = SparkSession \
    .builder \
    .appName("bigdatacoronatweets_broker_1") \
    .config("spark.sql.shuffle.partitions","2") \
    .getOrCreate()


# Create DataFrame representing the stream of input lines from connection to localhost:9092
data_stream = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "broker:9092") \
  .option("subscribe", "queueing.transactions") \
  .option("startingOffsets","earliest") \
  .load() \

tweet = Row("id", "created_at", "user_id", "location")

#Transforming





# data_stream_cleaned = data_stream \
#     .selectExpr("CAST(value AS STRING) as value") \
#     .select(
#         translate("value", "{", "").alias("a")) \
#     .select(
#         translate("a", "}", "") \
#     .alias("b")).select(
#         translate("b", ":", ",") \
#     .alias("c")).select(
#         translate("c", "'", "") \
#     .alias("d")).select(
#         translate("d", '"', "") \
#     .alias("e")).select(
#         translate("e", "id", "") \
#     .alias("f")).select(
#         translate("f", "created_at", "") \
#     .alias("g")).select(
#         translate("g", "user_id", "") \
#     .alias("h")).select(
#         translate("h", "location", "") \
#     .alias("i")).select(
#         split("i", ",").alias("i")) \
#     .select(['*']+[expr('i[' + str(x) + ']') for x in range(0, 4)]) \
#     .toDF("list", "id", "created_at", "user_id", "location") 




json_schema = spark.read.json(data_stream.rdd.map(lambda row: row.json)).schema
data_stream.withColumn('value', from_json(col('value'), json_shema))






    # .selectExpr("CAST(value AS STRING) as string_value") \
    # .flatMap(x = x.remove("{", "")) \
    # .flatMap(x = x.remove("}", "")) \
    # .flatMap(x = x.remove(":", ",")) \
    # .flatMap(x = x.split(",")) \
    # .flatMap(x.remove("id").remove("created_at").remove("user_id").remove("location")) \
    # .flatMap(x = tweet(x[0], x[1], x[2], x[3])) \
    # .selectExpr( "cast(id as long) id", "CAST(created_at as timestamp) created_at",  "cast(user_id as int) user_id", "cast(location as string) location") \
    # .toDF() \
    # .filter(col("created_at").gt(current_date())) \
    # .groupBy("location") \
    # .agg(count("id"), max("user_id"))  

query = df.writeStream \
    .format("memory") \
    .queryName("SpeedLayer") \
    .trigger(processingTime='60 seconds') \
    .outputMode("complete") \
    .start()

# query.awaitTermination()

def exportToPostgres():
    df = spark.sql("select * from SpeedLayer")

    #connection to postgres
    # df.write \
    #     .mode("overwrite") \
    #     .format("jdbc") \
    #     .option("url", "jdbc:postgresql://db:5432/postgres") \
    #     .option("driver", "org.postgresql.Driver") \
    #     .option("dbtable", "speedlayer") \
    #     .option("user", "postgres") \
    #     .option("password", "postgres") 

    mode = "overwrite"
    url = "jdbc:postgresql://db:5432/postgres"
    properties = {"user": "postgres","password": "postgres","driver": "org.postgresql.Driver"}
    df.write.jdbc(url=url, table="speedlayer", mode=mode, properties=properties)

while True:
    exportToPostgres()
    time.sleep(10)

# Stream funktionieren
# docker hochfahren docker compose up
# im log wird ausgegeben was ich printe
# docker logs mit nummer von dem gedönz
# docker ps ob alles läuft

# +---+-----+-----+---------+------+---------+-------------+
# |key|value|topic|partition|offset|timestamp|timestampType|
# +---+-----+-----+---------+------+---------+-------------+
# +---+-----+-----+---------+------+---------+-------------+

