from SyncData.config.db_config import get_db_config
from SyncData.config.spark_config import spark_connect_to_mysql, create_spark_session

jar_path = "../lib/mysql-connector-j-9.2.0.jar"

spark = create_spark_session(
    app_name="test",
    master_url="local[*]",
    executor_memory="4g",
    jars=[jar_path],
    log_level="ERROR"
)
db_config = get_db_config("mysql")
table_name = "Actors"
df = spark_connect_to_mysql(spark, db_config, table_name)
df.show()
df.printSchema()