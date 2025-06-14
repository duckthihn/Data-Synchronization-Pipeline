from pyspark.sql import DataFrame, SparkSession
from typing import Dict


class SparkWriteDatabases:
    def __init__(self, spark: SparkSession, db_config: Dict):
        self.spark = spark
        self.db_config = db_config

    def spark_write_mysql(self, df_write: DataFrame, table_name: str, jdbc_url: str, config: Dict,
                          mode: str = "append"):
        df_write.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("dbtable", table_name) \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .mode(mode) \
            .save()

        print(f"Spark - Successfully wrote data to MySQL table: {table_name}")

    def validate_spark_mysql(self, df_write: DataFrame, table_name: str, jdbc_url: str, config: Dict):
        # Read the table back from MySQL
        df_read = self.spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("dbtable", table_name) \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .load()

        if df_write.count() != df_read.count():
            print(f"VALIDATE ERROR: Data mismatch {df_read.count()} vs {df_write.count()} records between Spark and MySQL for table: {table_name}")
            return False
        else:
            print(f"VALIDATE SUCCESS: Data match {df_read.count()} vs {df_write.count()} records between Spark and MySQL for table: {table_name}")
            return True



    def spark_write_mongodb(self, df: DataFrame, database: str, collection: str, uri: str, mode: str = "overwrite"):
        df.write \
            .format("mongo") \
            .option("uri", uri) \
            .option("database", database) \
            .option("collection", collection) \
            .mode(mode) \
            .save()

        print(f"Spark - Successfully wrote data to MongoDB collection: {collection}")

    def write_all_database(self, df: DataFrame, mode: str = "append"):
        self.spark_write_mysql(
            df,
            table_name=self.db_config["mysql"]["table"],
            jdbc_url=self.db_config["mysql"]["jdbc_url"],
            config=self.db_config["mysql"]["config"],
            mode=mode
        )

        self.spark_write_mongodb(
            df,
            uri=self.db_config["mongodb"]["uri"],
            database=self.db_config["mongodb"]["database"],
            collection=self.db_config["mongodb"]["collection"],
            mode=mode
        )
        print("Wrote successfully to all databases")
