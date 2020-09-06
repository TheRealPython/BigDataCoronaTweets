import pyspark.sql

spark = SparkSession \
    .builder \
    .appName("Python Spark") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()