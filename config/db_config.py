import os
from dotenv import load_dotenv
from typing import Dict, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class DatabaseConfig:
    """Base configuration class for database connections."""

    def validate(self) -> None:
        """Validate that all required configuration values are present."""
        for key, value in self.__dict__.items():
            if value is None and not key.endswith('_optional'):
                raise ValueError(f"Missing required config for {key}")
        logger.info(f"Configuration validated for {self.__class__.__name__}")


@dataclass
class MySQLConfig(DatabaseConfig):
    """Configuration for MySQL database connection."""
    host: str
    port: int
    user: str
    password: str
    database: str
    jar_path: Optional[str] = None
    table: str = "Users"
    driver: str = "com.mysql.cj.jdbc.Driver"


@dataclass
class MongoDBConfig(DatabaseConfig):
    """Configuration for MongoDB database connection."""
    uri: str
    database: str
    jar_path: Optional[str] = None
    collection: str = "Users"


@dataclass
class RedisConfig(DatabaseConfig):
    """Configuration for Redis database connection."""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    database: Union[str, int] = 0
    jar_path: Optional[str] = None
    key_column: str = "id"
    decode_responses: bool = True


def load_environment_config(env_file_path: Optional[str] = None) -> None:
    if env_file_path is None:
        possible_paths = [
            Path.cwd() / ".env",
            Path.cwd() / "docker" / ".env",
            Path(__file__).parent.parent / "docker" / ".env"
        ]

        for path in possible_paths:
            if path.exists():
                env_file_path = str(path)
                break

        if env_file_path is None:
            logger.warning("No .env file found in common locations")
            return

    load_dotenv(dotenv_path=env_file_path)
    logger.info(f"Loaded environment configuration from {env_file_path}")


def get_db_config(env_file_path: Optional[str] = None) -> Dict[str, DatabaseConfig]:
    load_environment_config(env_file_path)

    try:
        config = {
            "mysql": MySQLConfig(
                host=os.getenv("MYSQL_HOST"),
                port=int(os.getenv("MYSQL_PORT")),
                user=os.getenv("MYSQL_ROOT_USER"),
                password=os.getenv("MYSQL_ROOT_PASSWORD"),
                database=os.getenv("MYSQL_DB"),
                jar_path=os.getenv("MYSQL_JAR_PATH")
            ),
            "mongodb": MongoDBConfig(
                uri=os.getenv("MONGO_URI"),
                database=os.getenv("MONGO_DB"),
                jar_path=os.getenv("MONGO_JAR_PATH")
            ),
            "redis": RedisConfig(
                host=os.getenv("REDIS_HOST"),
                port=int(os.getenv("REDIS_PORT")),
                username=os.getenv("REDIS_USER"),
                password=os.getenv("REDIS_PASSWORD"),
                database=os.getenv("REDIS_DB"),
                jar_path=os.getenv("REDIS_JAR_PATH")
            )
        }

        # Validate all configurations
        for db_name, db_config in config.items():
            try:
                db_config.validate()
            except ValueError as e:
                logger.error(f"Configuration error for {db_name}: {e}")
                raise

        return config

    except (ValueError, TypeError) as e:
        logger.error(f"Error creating database configuration: {e}")
        raise ValueError(f"Invalid database configuration: {e}")
