from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from SyncData.config.db_config import get_db_config
from SyncData.schema.schema_manager import create_mongodb_schema, validate_mongodb_schema

class MongoDBConnect:
    def __init__(self, uri, database):
        self.uri = uri
        self.database = database
        self.client = None
        self.db = None

    def __enter__(self):
        # Establish connection
        self.connect()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up the connection
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            # self.client.server_info()  # Test connection
            self.db = self.client[self.database]
            print(f"Connected to MongoDB database: {self.database}")
            return self.db
        except ConnectionFailure as e:
            print(f"MongoDB connection error: {e}")
            return None

    def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB.")

    def reconnect(self):
        self.disconnect()
        return self.connect()

def main():
    mongo_config = get_db_config()
    with MongoDBConnect(mongo_config["mongodb"].uri, mongo_config["mongodb"].database) as mongo_client:
        if mongo_client:
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

if __name__ == "__main__":
    main()