import os
from dotenv import load_dotenv
from typing import Dict
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    def validate(self) -> None:
        for key, value in self.__dict__.items():
            if value is None:
                raise ValueError(f"Missing config for {key}")

@dataclass
class MySQLConfig(DatabaseConfig):
    host : str
    port : int
    user : str
    password : str
    database : str

@dataclass
class MongoDBConfig(DatabaseConfig):
    uri : str
    database : str

@dataclass
class RedisConfig(DatabaseConfig):
    host: str
    port: int
    user: str
    password: str
    database: str


def get_db_config() -> Dict[str,DatabaseConfig]:
    # load .env file
    load_dotenv(dotenv_path="/home/duckthihn/PycharmProjects/DE-ETL/SyncData/docker/.env")

    config = {
        "mysql": MySQLConfig(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_ROOT_USER"),
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        ),
        "mongodb" : MongoDBConfig(
            uri = os.getenv("MONGO_URI"),
            database = os.getenv("MONGO_DB")
        ),
        "redis" : RedisConfig(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            user=os.getenv("REDIS_USER"),
            password=os.getenv("REDIS_PASSWORD"),
            database=os.getenv("REDIS_DB")
        )
    }

    for db, setting in config.items():
        setting.validate()

    return config