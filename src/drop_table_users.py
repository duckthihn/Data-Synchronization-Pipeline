from SyncData.config.db_config import get_db_config
from SyncData.database.mongo_connect import MongoDBConnect
from SyncData.database.mysql_connect import MySQLConnect
from SyncData.database.redis_connect import RedisConnect


def main():
    # Drop table Users in MySQL and MongoDB
    print("========================= DROP TABLE USERS ==================================")
    print("================================== MYSQL ==================================")
    db_name = config["mysql"].database
    with MySQLConnect(
            config["mysql"].host,
            config["mysql"].port,
            config["mysql"].user,
            config["mysql"].password
    ) as mysql_conn:
        connection, cursor = mysql_conn.connection, mysql_conn.cursor
        mysql_conn.select_database(db_name)

        cursor.execute("DROP TABLE IF EXISTS Users")

        changes = ["insert", "update", "delete"]

        for change in changes:
            cursor.execute(f"DROP TABLE IF EXISTS Users_{change}_before")
            cursor.execute(f"DROP TABLE IF EXISTS Users_{change}_after")
            cursor.execute(f"DROP TRIGGER IF EXISTS before_users_{change}")
            cursor.execute(f"DROP TRIGGER IF EXISTS after_users_{change}")

        connection.commit()
    print("================================== MONGO ==================================")
    with MongoDBConnect(
            config["mongodb"].uri,
            config["mongodb"].database,
    ) as mongo_client:
        mongo_client.Users.drop()


if __name__ == "__main__":
    config = get_db_config()
    main()
