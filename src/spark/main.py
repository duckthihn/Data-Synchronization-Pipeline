from spark_write_data import SparkWriteDatabases
from SyncData.config.db_config import get_db_config
from SyncData.config.spark_config import SparkConnect, get_spark_config
from pyspark.sql.types import *
from pyspark.sql.functions import col, lit


def main():
    db_configs = get_spark_config()

    jars = [
        "mysql:mysql-connector-java:8.0.33",
        "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1"
    ]

    spark_session = SparkConnect(
        app_name="spark_write_database",
        master_url="local[*]",
        executor_memory="2g",
        executor_cores=2,
        driver_memory="2g",
        num_executors=3,
        jar_packages=jars,
        # spark_conf=spark_conf,
        log_level="INFO"
    ).spark

    schema = StructType([
        StructField("actor", StructType([
            StructField("id", LongType(), False),
            StructField("login", StringType(), True),
            StructField("gravatar_id", StringType(), True),
            StructField("url", StringType(), True),
            StructField("avatar_url", StringType(), True),
            # StructField("spark", StringType(), False),
        ]), True),
        StructField("repo", StructType([
            StructField("id", LongType(), False),
            StructField("name", StringType(), True),
            StructField("url", StringType(), True),
        ]), True)
    ])

    # Read data
    df = spark_session.read.schema(schema).json("../../data/2015-03-01-17.json")

    # df.show()

    df_write_table_Users = df.withColumn(
        'spark_temp', lit('spark_write')
    ).select(
        col("actor.id").alias("user_id"),
        col("actor.login").alias("login"),
        col("actor.gravatar_id").alias("gravatar_id"),
        col("actor.url").alias("url"),
        col("actor.avatar_url").alias("avatar_url"),
        col("spark_temp").alias("spark_temp")
    )

    # df_write_table_Repositories = df.select(
    #     col("repo.id").alias("repo_id"),
    #     col("repo.name").alias("name"),
    #     col("repo.url").alias("url")
    # )

    spark_configs = get_spark_config()

    df_write = SparkWriteDatabases(spark_session, spark_configs)

    df_validate = SparkWriteDatabases(spark_session, spark_configs)

    df_write.write_all_database(df_write_table_Users, mode="append")

    df_validate.validate_spark_mysql(
        df_write=df_write_table_Users,
        table_name=db_configs["mysql"]["table"],
        jdbc_url=db_configs["mysql"]["jdbc_url"],
        config=db_configs["mysql"]["config"]
    )

    spark_session.stop()


if __name__ == "__main__":
    main()
