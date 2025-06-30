from SyncData.config.db_config import get_db_config
from SyncData.database.mongo_connect import MongoDBConnect
from SyncData.database.mysql_connect import MySQLConnect
from SyncData.database.schema_manager import create_mongodb_schema, validate_mongodb_schema, create_mysql_schema, \
    create_mysql_database, validate_mysql_schema, create_mysql_trigger


def main():
    # MongoDB
    print("================================= MONGODB =================================")
    with MongoDBConnect(
            config["mongodb"].uri,
            config["mongodb"].database,
    ) as mongo_client:
        create_mongodb_schema(mongo_client)
        mongo_client.Users.insert_one(
            {
                "user_id": 1,
                "login": "GoogleCodeExporter",
                "gravatar_id": "",
                "url": "https://api.github.com/users/GoogleCodeExporter",
                "avatar_url": "https://avatars.githubusercontent.com/u/9614759?"
            }
        )
        # validate_mongodb_schema(mongo_client)

    #  MySQL
    print("================================== MYSQL ==================================")
    db_name = config["mysql"].database
    with MySQLConnect(
            config["mysql"].host,
            config["mysql"].port,
            config["mysql"].user,
            config["mysql"].password
    ) as mysql_conn:
        connection, cursor = mysql_conn.connection, mysql_conn.cursor
        create_mysql_database(cursor, db_name)
        mysql_conn.select_database(db_name)
        create_mysql_schema(connection, cursor)

        # Create trigger in MySQL
        create_mysql_trigger(connection, cursor)

        # Use execute_query method instead of direct cursor execution
        cursor.execute(
            "INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (%s, %s, %s, %s, %s)",
            (1, 'GoogleCodeExporter', '', 'https://api.github.com/users/GoogleCodeExporter',
             'https://avatars.githubusercontent.com/u/9614759?')
        )

        cursor.execute(
            "UPDATE Users SET login = 'user1_update', gravatar_id = 'xxxx', url = 'abc.com', avatar_url = 'xyz.com' WHERE user_id = 1"
        )

        connection.commit()

        # Validate MySQL sql
        # validate_mysql_schema(cursor, db_name)


if __name__ == "__main__":
    config = get_db_config()
    main()
