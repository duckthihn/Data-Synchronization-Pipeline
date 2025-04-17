import redis
from redis.exceptions import RedisError

from SyncData.config.db_config import get_db_config


class RedisConnect:
    def __init__(self, host, port, db, password):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client = None

    def __enter__(self):
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True
            )
            self.client.ping() # verify connection
            print(f"Connected to Redis DB:{self.db}")
            return self.client
        except RedisError as e:
            print(f"Redis connection failed: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            try:
                self.client.close()
                print("Disconnected from Redis")
            except RedisError as e:
                print(f"Error while disconnecting from Redis: {e}")
