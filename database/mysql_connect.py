import mysql.connector
from mysql.connector import Error
import logging
from typing import Optional, List, Dict, Any, Tuple


class MySQLConnect:
    """
    A class to manage MySQL database connections with context management support.
    """

    def __init__(self, host: str, port: int, user: str, password: str):
        """
        Initialize a MySQL connection.

        Args:
            host: MySQL server hostname or IP
            port: MySQL server port
            user: MySQL username
            password: MySQL password
        """
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
            logging.info("MySQL connection established")
            return self
        except Error as e:
            logging.error(f"MySQL connection error: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.info("MySQL connection closed")

    def select_database(self, database_name: str) -> None:

        try:
            self.connection.database = database_name
            logging.info(f"Switched to database: {database_name}")
        except Error as e:
            logging.error(f"Error selecting database {database_name}: {e}")
            raise

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> None:
        """
        Execute a query without returning results.

        Args:
            query: SQL query to execute
            params: Parameters for the query
        """
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            logging.info(f"Query executed successfully: {query[:50]}...")
        except Error as e:
            logging.error(f"Error executing query: {e}")
            self.connection.rollback()
            raise

    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:

        try:
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchall()
            logging.info(f"Fetched {len(result)} rows from query: {query[:50]}...")
            return result
        except Error as e:
            logging.error(f"Error fetching data: {e}")
            raise
