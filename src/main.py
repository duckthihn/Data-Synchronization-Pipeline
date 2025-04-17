from SyncData.config.db_config import get_db_config
from SyncData.database.mongo_connect import MongoDBConnect
from SyncData.database.mysql_connect import MySQLConnect
from SyncData.database.redis_connect import RedisConnect
from SyncData.schema.schema_manager import create_mongodb_schema, validate_mongodb_schema, create_mysql_schema, \
    create_mysql_database, validate_mysql_schema


def main():
    # MongoDB
    print("================================= MONGODB =================================")
    with MongoDBConnect(config["mongodb"].uri, config["mongodb"].database) as mongo_client:
        create_mongodb_schema(mongo_client)
        # mongo_client.Users.insert_one(
        #     {
        #         "user_id": 9614759,
        #         "login": "GoogleCodeExporter",
        #         "gravatar_id": "",
        #         "url": "https://api.github.com/users/GoogleCodeExporter",
        #         "avatar_url": "https://avatars.githubusercontent.com/u/9614759?"
        #     }
        # )
        # print("---- Inserted to MongoDB ----")
        validate_mongodb_schema(mongo_client)

    #  MySQL
    print("================================== MYSQL ==================================")
    db_name = config["mysql"].database
    with (MySQLConnect(
            config["mysql"].host,
            config["mysql"].port,
            config["mysql"].user,
            config["mysql"].password)
    as mysql_conn):
        connection, cursor = mysql_conn.connection, mysql_conn.cursor
        create_mysql_database(cursor, db_name)
        mysql_conn.select_database(db_name)
        create_mysql_schema(connection, cursor)
        validate_mysql_schema(cursor, db_name)

        # cursor.execute("INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9614759, 'GoogleCodeExporter', '', 'https://api.github.com/users/GoogleCodeExporter', 'https://avatars.githubusercontent.com/u/9614759?');")
        connection.commit()

    # Redis
    print("================================== REDIS ==================================")
    with RedisConnect(
        config["redis"].host,
        config["redis"].port,
        config["redis"].database,
        config["redis"].password
    ) as redis_client:
        redis_client.set("hello", "world")
        value = redis_client.get("hello")
        print(f"Value from Redis: {value}")


if __name__ == "__main__":
    config = get_db_config()
    main()
