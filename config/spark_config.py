from dask.dataframe import DataFrame
from pyspark.sql import SparkSession
from typing import Optional, List, Dict
import os
from SyncData.config.db_config import get_db_config

"""
    THIS FILE COVERS SPARK FUNCTIONS IN RELATING TO WRITE & READ DATA FROM DATABASES
    IT ALSO INCLUDES DATA VALIDATION WHEN IT IS IMPORTED TO THE DATABASE 
"""


class SparkConnect():
    def __init__(
            self,
            app_name: str,
            master_url: str = "local[*]",
            # thực tế là đi làm ko được chạy trên local =>> phải link vào con master
            executor_memory: Optional[str] = "4g",
            executor_cores: Optional[int] = 2,
            driver_memory: Optional[str] = "2g",
            num_executors: Optional[int] = 3,
            jar_packages: Optional[List[str]] = None,
            spark_conf: Optional[Dict[str, str]] = None,
            log_level: str = "WARN"
    ):
        self.app_name = app_name
        self.spark = self.create_spark_session(master_url, executor_memory, executor_cores, driver_memory,
                                               num_executors, jar_packages, spark_conf, log_level)

    def create_spark_session(
            self,
            # app_name: str,
            master_url: str = "local[*]",
            executor_memory: Optional[str] = "4g",
            executor_cores: Optional[int] = 2,
            driver_memory: Optional[str] = "2g",
            num_executors: Optional[int] = 3,
            jar_packages: Optional[List[str]] = None,
            spark_conf: Optional[Dict[str, str]] = None,
            log_level: str = "WARN"
    ) -> SparkSession:

        builder = SparkSession.builder \
            .appName(self.app_name) \
            .master(master_url)

        if executor_memory:
            builder.config("spark.executor.memory", executor_memory)

        if executor_cores:
            builder.config("spark.executor.cores", executor_cores)
        if driver_memory:
            builder.config("spark.driver.memory", driver_memory)
        if num_executors:
            builder.config("spark.executor.instances", num_executors)

        # if jars:
        #     jars_path = ",".join([os.path.abspath(jar) for jar in jars])
        #     builder.config("spark.jars.packages", jars_path)

        if jar_packages:
            jar_packages_url = ",".join([jar_package for jar_package in jar_packages])
            builder.config("spark.jars.packages", jar_packages_url)

        # {"spark.sql.shuffle.partitions": "10"}
        if spark_conf:
            for key, value in spark_conf.items():
                builder.config(key, value)

        spark = builder.getOrCreate()

        spark.sparkContext.setLogLevel(log_level)

        return spark

    def stop(self):
        if self.spark:
            self.spark.stop()
            print("Stop Spark Session")


def get_spark_config() -> Dict:
    db_configs = get_db_config()

    return {
        "mysql": {
            "table": db_configs["mysql"].table,
            "jdbc_url": f"jdbc:mysql://{db_configs["mysql"].host}:{db_configs["mysql"].port}/{db_configs['mysql'].database}",
            "config": {
                "host": db_configs["mysql"].host,
                "port": db_configs["mysql"].port,
                "user": db_configs["mysql"].user,
                "password": db_configs["mysql"].password,
                "database": db_configs["mysql"].database,
            },
        },
        "mongodb": {
            "database": db_configs["mongodb"].database,
            "uri": db_configs["mongodb"].uri,
            "collection": db_configs["mongodb"].collection
        },
        "redis": {

        }
    }


if __name__ == "__main__":
    config = get_spark_config()
    print(config)
