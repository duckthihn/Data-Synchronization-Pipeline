from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

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