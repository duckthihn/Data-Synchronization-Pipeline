import pymongo
from pathlib import Path
from mysql.connector.errors import Error


### MongoDB
def create_mongodb_schema(db):
    if "Users" not in db.list_collection_names():
        db.create_collection(
            "Users",
            validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["user_id", "login"],
                    "properties": {
                        "user_id": {
                            "bsonType": "int"
                        },
                        "login": {
                            "bsonType": "string"
                        },
                        "gravatar_id": {
                            "bsonType": ["string", "null"]
                        },
                        "url": {
                            "bsonType": ["string", "null"]
                        },
                        "avatar_url": {
                            "bsonType": ["string", "null"]
                        }
                    }
                }
            }
        )

        db["Users"].create_index("user_id", unique=True)
        print("Executed MongoDB schema successfully")
    else:
        print("Schema already exists")


def validate_mongodb_schema(db):
    collections = db.list_collection_names()
    if "Users" not in collections:
        raise ValueError("Missing collections in MongoDB")

    user = db.Users.find_one({"user_id": 9614759})

    if not user:
        raise ValueError("user_id not found in MongoDB")

    print("MongoDB schema validated successfully")


### MySQL
def create_mysql_database(cursor, database_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"Database {database_name} created or existed!")


SQL_FILE_PATH = Path("/home/duckthihn/PycharmProjects/DE-ETL/SyncData/schema/schema.sql")


def create_mysql_schema(connection, cursor):
    try:
        with open(SQL_FILE_PATH, "r") as file:
            sql_script = file.read()

            sql_queries = [query.strip() for query in sql_script.split(';') if query.strip()]

            for query in sql_queries:
                try:
                    cursor.execute(query)
                    print(f"Executed query: {query[:30]}...")
                except Error as err:
                    print(f"Error executing query: {err}")
            connection.commit()
            print("SQL schema executed successfully.")
    except Exception as e:
        print(f"Failed to execute SQL file: {e}")


def validate_mysql_schema(cursor, database):
    cursor.execute("SHOW DATABASES LIKE %s", (database,))
    if not cursor.fetchone():
        raise ValueError(f"Database '{database}' does not exist.")
    print(f"Database '{database}' found.")

    cursor.execute(f"USE {database}")

    required_tables = ['Users', 'Repositories']
    for table in required_tables:
        cursor.execute(f"SHOW TABLES LIKE %s", (table,))
        if not cursor.fetchone():
            raise ValueError(f"Table '{table}' is missing in the database.")
        print(f"Table '{table}' exists.")

    # Check records
    cursor.execute("SELECT * FROM Users WHERE user_id = 9614759")
    user = cursor.fetchone()
    if user is None:
        raise ValueError("User not found")
    print(user)

    print("MySQL schema validated successfully.")


def create_redis_schema(client):
    try:
        client.flushdb()  # drop database
        client.set("user:1:login", "GoogleCodeExporter")
        client.set("user:1:gravatar_id", "")
        client.set("user:1:url", "https://api.github.com/users/GoogleCodeExporter")
        client.set("user:1:avatar_url", "https://avatars.githubusercontent.com/u/9614759?")
        client.sadd("user_id", "user:1")
        print(f"Add data to Redis successfully")
    except Exception as e:
        raise Exception(f"Failed to add data to Redis: {e}")


def validate_redis_schema(client):
    if not client.get("user:1:login") == "GoogleCodeExporter":
        raise ValueError(f"Value login not found in Redis")

    if not client.sismember("user_id", "user:1"):
        raise ValueError(f"User not set in Redis")

    print("Redis validated schema")
