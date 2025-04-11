import mysql.connector
from pathlib import Path

from SyncData.config.db_config import get_db_config

SQL_FILE_PATH = Path("/home/duckthihn/PycharmProjects/DE-ETL/SyncData/schema/schema.sql")

def connect_to_mysql(db_config):
    try:
        allowed_keys = {"host", "port", "database", "user", "password"}
        config = {k: v for k, v in db_config.items() if k in allowed_keys}
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(cursor, database_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"Database {database_name} created or existed!")

def execute_schema(cursor, sql_file_path):
    with open(sql_file_path, 'r') as file:
        sql_file = file.read()

    # sql_queries = sql_file.split(';')
    #
    # for query in sql_queries:
    #     if query.strip():
    #         try:
    #             cursor.execute(query)
    #             print(f"Executed query: {query[:30]}...")
    #         except mysql.connector.Error as err:
    #             print(f"Error: {err}")

    sql_queries = [query.strip() for query in sql_file.split(';') if query.strip()]

    for query in sql_queries:
        try:
            cursor.execute(query)
            print(f"Executed query: {query[:50]}...")
        except mysql.connector.Error as err:
            print(f"Error executing query: {query[:50]}... -> {err}")


def main():
    # get config from .env
    mysql_config = get_db_config("mysql")

    # connect to mysql db
    conn = connect_to_mysql(mysql_config)
    cursor = conn.cursor()

    DATABASE_NAME = mysql_config["database"]
    # create database
    create_database(cursor, DATABASE_NAME)

    # USE database
    conn.database = DATABASE_NAME

    # execute_schema
    execute_schema(cursor, SQL_FILE_PATH)

    # commit and clean up
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()