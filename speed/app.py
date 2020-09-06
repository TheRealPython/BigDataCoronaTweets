from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
import time

spark = SparkSession \
    .builder \
    .config("spark.sql.shuffle.partitions","2") \
    .appName("DerInderGenerator") \
    .getOrCreate()

# Create DataFrame representing the stream of input lines from connection to localhost:9092
data_stream = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "broker:9092") \
  .option("subscribe", "queueing.transactions") \
  .option("startingOffsets","earliest") \
  .load()

# Split the datastream into words
words = data_stream.select(
   explode(
       split(data_stream.value, " ")
   ).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()

 # Start running the query that prints the running counts to the console
query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .trigger(processingTime='60 seconds') \
    .format("console") \
    .start()

query.awaitTermination()

# Stream funktionieren
# docker hochfahren docker compose up
# im log wird ausgegeben was ich printe
# docker logs mit nummer von dem gedönz
# docker ps ob alles läuft