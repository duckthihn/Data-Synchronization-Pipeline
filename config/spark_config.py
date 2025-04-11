from dask.dataframe import DataFrame
from pyspark.sql import SparkSession
from typing import Optional, List, Dict
import os


def create_spark_session(
        app_name: str,
        master_url: str = "local[*]",
        executor_memory: Optional[str] = "4g",
        executor_cores: Optional[int] = 2,
        driver_memory: Optional[str] = "2g",
        num_executors: Optional[int] = 3,
        jars: Optional[List[str]] = None,
        spark_conf: Optional[Dict[str,str]] = None,
        log_level: str = "WARN"
) -> SparkSession:
    builder = SparkSession.builder \
    .appName(app_name) \
    .master(master_url) \

    if executor_memory:
        builder.config("spark.executor.memory", executor_memory)
    if executor_cores:
        builder.config("spark.executor.cores", executor_cores)
    if driver_memory:
        builder.config("spark.driver.memory", driver_memory)
    if num_executors:
        builder.config("spark.executor.instances", num_executors)

    if jars:
        jars_path = ",".join([os.path.abspath(jar) for jar in jars])
        builder.config("spark.jars", jars_path)

    # {"spark.sql.shuffle.partitions": "10"}
    if spark_conf:
        for key, value in spark_conf.items():
            builder.config(key,value)

    spark = builder.getOrCreate()

    spark.sparkContext.setLogLevel(log_level)

    return spark

"""
spark = create_spark_session(
    app_name="test",
    master_url="local[*]",
    executor_memory="4g",
    executor_cores=2,
    driver_memory="4g",
    num_executors=4,
    jars=None,
    spark_conf={"spark.sql.shuffle.partitions": "10"},
    log_level="ERROR"
)

data = [["dat",18], ["sonbui",21], ["toan", 22]]
df = spark.createDataFrame(data, ["name", "age"])
df.show()
df.printSchema()
"""

# jars = [
#     "../lib/mongodb-jdbc-2.2.2-all.jar",
#     "../lib/mysql-connector-j-9.2.0.jar",
#     "../lib/redis-jdbc-driver-1.5.jar"
# ]

# spark = create_spark_session(
#     app_name="test",
#     master_url="local[*]",
#     executor_memory="4g",
#     executor_cores=2,
#     driver_memory="4g",
#     num_executors=4,
#     jars=jars,
#     spark_conf={"spark.sql.shuffle.partitions": "10"},
#     log_level="INFO"
# )


# CONNECT TO MYSQL AND READ DATA FROM TABLE
def spark_connect_to_mysql(
        spark: SparkSession,
        config: Dict[str, str],
        table_name: str
) -> DataFrame:
    df = spark.read \
        .format("jdbc") \
        .option("url", config["url"]) \
        .option("driver", config["driver"]) \
        .option("dbtable", table_name) \
        .option("user", config["user"]) \
        .option("password", config["password"]) \
        .load()

    return df