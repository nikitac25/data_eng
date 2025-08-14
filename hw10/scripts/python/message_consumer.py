from pyspark.sql import SparkSession
from pyspark.sql import functions as F, types as T
import constants

# simple schema
schema = T.StructType([
    T.StructField("user_id", T.IntegerType(), True),
    T.StructField("domain", T.StringType(), True),
    T.StructField("created_at", T.StringType(), True),
    T.StructField("page_title", T.StringType(), True),
])

# spark session
spark = (
    SparkSession.builder
    .appName("wikipedia stream")
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,"
            "com.datastax.spark:spark-cassandra-connector_2.12:3.4.1")
    .config("spark.sql.streaming.checkpointLocation", "/tmp/spark-checkpoint")
    .config("spark.cassandra.connection.host", constants.CASSANDRA_HOST)
    .config("spark.cassandra.connection.port", constants.CASSANDRA_PORT)
    .getOrCreate()
)

print(f"reading from kafka topic: {constants.KAFKA_TOPIC}")

# read stream once, fail loud if it doesn't work
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", constants.BOOTSTRAP_SERVERS)
    .option("subscribe", constants.KAFKA_TOPIC)
    .option("startingOffsets", "latest")
    .option("failOnDataLoss", "false")
    .load()
)

parsed = (
    df.select(F.from_json(F.col("value").cast("string"), schema).alias("x"))
      .select(
          F.col("x.user_id"),
          F.col("x.domain"),
          F.to_timestamp(F.col("x.created_at")).alias("created_at"),
          F.col("x.page_title"),
      )
)

print(f"writing to cassandra: {constants.CASSANDRA_KEYSPACE}.{constants.CASSANDRA_TABLE}")

query = (
    parsed.writeStream
    .format("org.apache.spark.sql.cassandra")
    .outputMode("append")
    .options(
        table=constants.CASSANDRA_TABLE,
        keyspace=constants.CASSANDRA_KEYSPACE
    )
    .option("checkpointLocation", "/tmp/spark-checkpoint")
    .start()
)

query.awaitTermination()
