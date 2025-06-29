from pyspark.sql import DataFrame, SparkSession
from typing import Dict

from pyspark.sql.functions import col

from SyncData.config.db_config import get_db_config
from SyncData.database.mongo_connect import MongoDBConnect
from SyncData.database.mysql_connect import MySQLConnect


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

        # Filter both DataFrames where spark_temp = 'spark_write'
        df_write_spark = df_write.filter("spark_temp = 'spark_write'")
        df_read_spark = df_read.filter("spark_temp = 'spark_write'")

        # Align column order
        columns = df_write_spark.columns
        df_write_spark = df_write_spark.select(columns)
        df_read_spark = df_read_spark.select(columns)

        write_count = df_write_spark.count()
        read_count = df_read_spark.count()

        def find_and_write_missing(df_spark_write: DataFrame, df_read_database: DataFrame):
            missing_rows = df_spark_write.exceptAll(df_read_database)
            missing_count = missing_rows.count()
            if missing_count > 0:
                print(f"⚠️ Missing {missing_count} records detected in MySQL. Writing them now...")
                missing_rows.write \
                    .format("jdbc") \
                    .option("url", jdbc_url) \
                    .option("driver", "com.mysql.cj.jdbc.Driver") \
                    .option("dbtable", table_name) \
                    .option("user", config["user"]) \
                    .option("password", config["password"]) \
                    .mode("append") \
                    .save()
                print(f"✅ Auto-write complete: {missing_count} records added to {table_name}")
            else:
                print("✅ No missing records detected.")

        # Validate and write missing records if needed
        if write_count != read_count:
            print(
                f"❌ MYSQL VALIDATE ERROR: Data mismatch {read_count} vs {write_count} records for table: {table_name}")
            find_and_write_missing(df_write_spark, df_read_spark)
            result = False
        else:
            print(f"✅ MYSQL VALIDATE SUCCESS: Data match {read_count} vs {write_count} records for table: {table_name}")
            find_and_write_missing(df_write_spark, df_read_spark)
            result = True

        # Drop spark_temp column after validating
        try:
            with MySQLConnect(config["host"], config["port"], config["user"], config["password"]) as mysql_client:
                conn, cursor = mysql_client.connection, mysql_client.cursor
                database_name = "github_data"
                conn.database = database_name
                cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN spark_temp")
                conn.commit()
                print("MySQL: Dropped spark_temp column")
        except:
            raise Exception("Error connecting to MySQL database.")

        return result

    def spark_write_mongodb(self, df: DataFrame, database: str, collection: str, uri: str, mode: str = "overwrite"):
        df.write \
            .format("mongo") \
            .option("uri", uri) \
            .option("database", database) \
            .option("collection", collection) \
            .mode(mode) \
            .save()

        print(f"Spark - Successfully wrote data to MongoDB collection: {collection}")

    def validate_spark_mongodb(self, df_write: DataFrame, database: str, collection: str, uri: str):
        query = {"spark_temp": 'spark_write'}

        df_read = self.spark.read \
            .format("mongo") \
            .option("uri", uri) \
            .option("database", database) \
            .option("collection", collection) \
            .option("pipeline", str([{"$match": query}])) \
            .load()

        df_read = df_read.select(
            col("user_id"),
            col("login"),
            col("gravatar_id"),
            col("url").alias("url"),
            col("avatar_url"),
            # Add spark_temp to validate append data from spark
            col("spark_temp")
        )

        # df_read.printSchema()

        def find_and_write_missing(df_spark_write: DataFrame, df_read_database: DataFrame):
            missing_rows = df_spark_write.exceptAll(df_read_database)
            missing_count = missing_rows.count()
            # missing_rows.printSchema()
            if missing_count > 0:
                print(f"⚠️ Missing {missing_count} records detected in MySQL. Writing them now...")
                missing_rows.write \
                    .format("mongo") \
                    .option("uri", self.db_config["mongodb"]["uri"]) \
                    .option("database", self.db_config["mongodb"]["database"]) \
                    .option("collection", self.db_config["mongodb"]["collection"]) \
                    .mode("append") \
                    .save()
                print(f"✅ Auto-write complete: {missing_count} records added to {collection}")
            else:
                print("✅ No missing records detected.")

        # Filter both DataFrames where spark_temp = 'spark_write'
        df_write_spark = df_write.filter("spark_temp = 'spark_write'")
        df_read_spark = df_read.filter("spark_temp = 'spark_write'")

        # Align column order
        columns = df_write_spark.columns
        df_write_spark = df_write_spark.select(columns)
        df_read_spark = df_read_spark.select(columns)

        write_count = df_write_spark.count()
        read_count = df_read_spark.count()

        # Validate and write missing records if needed
        if write_count != read_count:
            print(
                f"❌ MONGODB VALIDATE ERROR: Data mismatch {read_count} vs {write_count} records for table: {collection}")
            find_and_write_missing(df_write_spark, df_read_spark)
            result = False
        else:
            print(
                f"✅ MONGODB VALIDATE SUCCESS: Data match {read_count} vs {write_count} records for table: {collection}")
            find_and_write_missing(df_write_spark, df_read_spark)
            result = True

        # Drop spark_temp column in Mongodb using python
        with MongoDBConnect(
                uri,
                database,
        ) as mongo_client:
            mongo_client[collection].update_many({}, {"$unset": {"spark_temp": ""}})

        return result

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
        print("Spark wrote successfully to all databases")

    def validate_spark_write_all_databases(self, df: DataFrame):
        self.validate_spark_mysql(
            df,
            table_name=self.db_config["mysql"]["table"],
            jdbc_url=self.db_config["mysql"]["jdbc_url"],
            config=self.db_config["mysql"]["config"])
        self.validate_spark_mongodb(
            df,
            uri=self.db_config["mongodb"]["uri"],
            database=self.db_config["mongodb"]["database"],
            collection=self.db_config["mongodb"]["collection"])

        print("Validated successfully to all databases")
