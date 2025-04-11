import redis

from SyncData.config.db_config import get_db_config


def connect_to_redis(db_config):
    return redis.Redis(
        host=db_config["host"],
        port=db_config["port"],
        decode_responses=True
    )

redis_config = get_db_config("redis")

print(connect_to_redis(redis_config))