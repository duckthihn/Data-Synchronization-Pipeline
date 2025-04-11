from dotenv import load_dotenv
import os
from urllib.parse import urlparse


def parse_url(db_url, strip_prefix=None):
    if strip_prefix and db_url.startswith(strip_prefix):
        db_url = db_url[len(strip_prefix):]

    parsed = urlparse(db_url)
    return {
        "host": parsed.hostname,
        "port": parsed.port,
        "database": parsed.path.strip("/") if parsed.path else None
    }


def get_db_config(db_type):
    # load .env
    load_dotenv(dotenv_path="../docker/.env")

    match db_type:
        case "mysql":
            env_var = "MYSQL_URL"
            jdbc_url = os.getenv(env_var)
            if not jdbc_url:
                raise ValueError(f"Missing {env_var} in .env")

            info = parse_url(jdbc_url, strip_prefix="jdbc:")
            info.update({
                "user": os.getenv("MYSQL_ROOT_USER"),
                "password": os.getenv("MYSQL_ROOT_PASSWORD"),
                "url": os.getenv("MYSQL_URL"),
                "driver": os.getenv("MYSQL_DRIVER")
            })
            return info

        case "mongodb":
            env_var = "MONGO_URL"
            mongo_url = os.getenv(env_var)
            if not mongo_url:
                raise ValueError(f"Missing {env_var} in .env")

            info = parse_url(mongo_url)
            info.update({
                "user": os.getenv("MONGO_INITDB_ROOT_USERNAME"),
                "password": os.getenv("MONGO_INITDB_ROOT_PASSWORD")
            })
            return info

        case "redis":
            env_var = "REDIS_URL"
            redis_url = os.getenv(env_var)
            if not redis_url:
                raise ValueError(f"Missing {env_var} in .env")

            return parse_url(redis_url)

        case _:
            raise ValueError(f"Unknown db_type: {db_type}")
