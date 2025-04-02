import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "rootpassword",
    "database": "github_data"
}

sql_file_path = "/home/duckthihn/PycharmProjects/DE-ETL/SyncData/sql/schema.sql"

try:
    conn = mysql.connector.connect(**db_config)

    if conn.is_connected():
        print("Successfully connected to the database")

    cursor = conn.cursor()

    with open(sql_file_path, 'r') as file:
        sql_file = file.read()

    sql_queries = sql_file.split(';')

    for query in sql_queries:
        if query.strip():
            try:
                cursor.execute(query)
                print(f"Executed query: {query[:30]}...")
            except mysql.connector.Error as err:
                print(f"Error: {err}")

    conn.commit()

    cursor.close()
    conn.close()
    print("schema.sql file executed succesfully")


except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")