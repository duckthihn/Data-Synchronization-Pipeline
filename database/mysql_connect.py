import mysql.connector
from mysql.connector import Error
from SyncData.config.db_config import get_db_config
from SyncData.schema.schema_manager import create_mysql_database, create_mysql_schema, validate_mysql_schema
from pathlib import Path

class MySQLConnect:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("MySQL connection established")
            return self
        except Error as e:
            print(f"MySQL connection error: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("MySQL connection closed")

    def select_database(self, database_name):
        self.connection.database = database_name
        print(f"Switched to database: {database_name}")

def main():
    SQL_FILE_PATH = Path("/home/duckthihn/PycharmProjects/DE-ETL/SyncData/schema/schema.sql")
    mysql_config = get_db_config()
    db_name = mysql_config["mysql"].database
    with (MySQLConnect(
            mysql_config["mysql"].host,
            mysql_config["mysql"].port,
            mysql_config["mysql"].user,
            mysql_config["mysql"].password)
    as mysql_conn):

        print(mysql_conn.connection)
        print(mysql_conn.cursor)


        create_mysql_database(mysql_conn.cursor, db_name)
        mysql_conn.select_database(db_name)
        create_mysql_schema(mysql_conn.connection, mysql_conn.cursor, SQL_FILE_PATH)
        validate_mysql_schema(mysql_conn.cursor, db_name)

if __name__ == "__main__":
    main()