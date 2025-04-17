import mysql.connector
from mysql.connector import Error

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