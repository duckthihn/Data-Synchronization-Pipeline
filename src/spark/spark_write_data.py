from pyspark.sql import DataFrame, SparkSession
from typing import Dict
from SyncData.config.spark_config import get_spark_config


class SparkWriteDatabases:
    def __init__(self, spark: SparkSession, db_config: Dict):
        self.spark = spark
        self.db_config = db_config

    def spark_write_mysql(self, df: DataFrame, table_name: str, jdbc_url: str, config: Dict, mode: str = "append"):
        if mode == "append":
            # For append mode, use MySQL's INSERT IGNORE syntax to handle duplicate keys
            # This is done by setting a custom insertStatement property

            # Get column names for the INSERT statement
            columns = df.columns
            columns_str = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(columns))

            # Create an INSERT IGNORE statement
            insert_statement = f"INSERT IGNORE INTO {table_name} ({columns_str}) VALUES ({placeholders})"

            df.write \
                .format("jdbc") \
                .option("url", jdbc_url) \
                .option("driver", "com.mysql.cj.jdbc.Driver") \
                .option("dbtable", table_name) \
                .option("user", config["user"]) \
                .option("password", config["password"]) \
                .option("insertStatement", insert_statement) \
                .mode("append") \
                .save()

            print(f"Spark Wrote data to MySQL table: {table_name} with INSERT IGNORE")
        else:
            # Use standard write method for other modes
            df.write \
                .format("jdbc") \
                .option("url", jdbc_url) \
                .option("driver", "com.mysql.cj.jdbc.Driver") \
                .option("dbtable", table_name) \
                .option("user", config["user"]) \
                .option("password", config["password"]) \
                .mode(mode) \
                .save()

            print(f"Spark Wrote data to MySQL table: {table_name}")


    def write_all_database(self, df: DataFrame, mode: str = "append"):
        self.spark_write_mysql(
            df,
            table_name=self.db_config["mysql"]["table"],
            jdbc_url=self.db_config["mysql"]["jdbc_url"],
            config=self.db_config["mysql"]["config"],
            mode=mode
        )
        print("Wrote successfully to all databases")
