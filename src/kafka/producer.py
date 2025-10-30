from SyncData.config.db_config import get_db_config
from SyncData.database.mysql_connect import MySQLConnect
import datetime
import json
from kafka import KafkaProducer


def get_data_trigger(mysql_conn, db_name, last_timestamp):
    try:
        connection, cursor = mysql_conn.connection, mysql_conn.cursor
        mysql_conn.select_database(db_name)

        query = "SELECT * FROM Users_log_after"

        if last_timestamp:
            query += " WHERE log_timestamp > %s"
            cursor.execute(query, (last_timestamp,))
        else:
            cursor.execute(query)

        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        # Convert datetime to string
        for row in data:
            for key, value in row.items():
                if isinstance(value, datetime.datetime):
                    row[key] = value.isoformat()

        connection.commit()

        # Get the latest timestamp
        new_timestamp = max(
            (row['log_timestamp'] for row in data),
            default=last_timestamp
        ) if data else last_timestamp

        return data, new_timestamp

    except Exception as e:
        print(f"Error getting data from {db_name}: {e}")
        return [], last_timestamp


def main():
    config = get_db_config()
    db_name = config["mysql"].database

    last_timestamp = None

    # Producer for kafka
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )

    running = True
    while running:
        with MySQLConnect(
                config["mysql"].host,
                config["mysql"].port,
                config["mysql"].user,
                config["mysql"].password
        ) as mysql_conn:
            data, new_timestamp = get_data_trigger(mysql_conn, db_name, last_timestamp)
            last_timestamp = new_timestamp

            topic = "users"

            for record in data:
                producer.send(topic, record)

                print(record)
        producer.flush()


if __name__ == "__main__":
    main()
