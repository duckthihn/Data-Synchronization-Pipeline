from spark_write_data import SparkWriteDatabases
from SyncData.config.db_config import get_db_config
from SyncData.config.spark_config import SparkConnect, get_spark_config
from pyspark.sql.types import *
from pyspark.sql.functions import col


def main():
    db_configs = get_db_config()

    jar = [
        db_configs["mysql"].jar_path
    ]

    spark_conf = {
        "spark.jar.package": (
            "mysql:mysql-connector-java:9.2.0"
        )

    }


    spark_session = SparkConnect(
        app_name="spark_write_database",
        master_url="local[*]",
        executor_memory="4g",
        executor_cores=4,
        driver_memory="4g",
        num_executors=4,
        jars=jar,
        spark_conf=spark_conf,
        log_level="INFO"
    ).spark

    schema = StructType([
        StructField("actor", StructType([
            StructField("id", LongType(), False),
            StructField("login", StringType(), True),
            StructField("gravatar_id", StringType(), True),
            StructField("url", StringType(), True),
            StructField("avatar_url", StringType(), True),

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

    df_write_table_Users = df.select(
        col("actor.id").alias("user_id"),
        col("actor.login").alias("login"),
        col("actor.gravatar_id").alias("gravatar_id"),
        col("actor.url").alias("url"),
        col("actor.avatar_url").alias("avatar_url")
    )

    # df_write_table_Repositories = df.select(
    #     col("repo.id").alias("repo_id"),
    #     col("repo.name").alias("name"),
    #     col("repo.url").alias("url")
    # )

    spark_configs = get_spark_config()

    df_write = SparkWriteDatabases(spark_session, spark_configs)

    df_write.write_all_database(df_write_table_Users.coalesce(10), mode="overwrite")

    spark_session.stop()


if __name__ == "__main__":
    main()
