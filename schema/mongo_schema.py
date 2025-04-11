from pymongo import MongoClient
from SyncData.config.db_config import get_db_config

def connect_to_mongodb(db_config):
    try:
        client = MongoClient(
            host=db_config["host"],
            port=db_config["port"],
            username=db_config["user"],
            password=db_config["password"],
            authSource=db_config.get("authSource", "admin")
        )
        db = client[db_config["database"]]
        print(f"✅ Connected to MongoDB database: {db.name}")
        return db
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        return None

def setup_collections(db):
    # Actors
    db.create_collection("Actors", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["actor_id", "login"],
            "properties": {
                "actor_id": {"bsonType": "long"},
                "login": {"bsonType": "string"},
                "gravatar_id": {"bsonType": "string"},
                "url": {"bsonType": "string"},
                "avatar_url": {"bsonType": "string"},
            }
        }
    })

    # Repositories
    db.create_collection("Repositories", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["repo_id", "name", "url"],
            "properties": {
                "repo_id": {"bsonType": "long"},
                "name": {"bsonType": "string"},
                "url": {"bsonType": "string"},
            }
        }
    })

    # Issues
    db.create_collection("Issues", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["issue_id", "repo_id", "user_id"],
            "properties": {
                "issue_id": {"bsonType": "long"},
                "issue_number": {"bsonType": "int"},
                "title": {"bsonType": "string"},
                "body": {"bsonType": "string"},
                "state": {"bsonType": "string"},
                "locked": {"bsonType": "bool"},
                "html_url": {"bsonType": "string"},
                "comments_count": {"bsonType": "int"},
                "created_at": {"bsonType": "date"},
                "updated_at": {"bsonType": "date"},
                "closed_at": {"bsonType": "date"},
                "user_id": {"bsonType": "long"},
                "repo_id": {"bsonType": "long"}
            }
        }
    })

    # Comments
    db.create_collection("Comments", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["comment_id", "issue_id", "user_id"],
            "properties": {
                "comment_id": {"bsonType": "long"},
                "issue_id": {"bsonType": "long"},
                "user_id": {"bsonType": "long"},
                "body": {"bsonType": "string"},
                "created_at": {"bsonType": "date"},
                "updated_at": {"bsonType": "date"}
            }
        }
    })

    # Payloads
    db.create_collection("Payloads", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["payload_id"],
            "properties": {
                "payload_id": {"bsonType": "long"},
                "action": {"bsonType": "string"},
                "issue_id": {"bsonType": "long"},
                "comment_id": {"bsonType": "long"}
            }
        }
    })

    print("✅ Collections created with validation rules!")

if __name__ == "__main__":
    db_config = get_db_config("mongodb")
    db = connect_to_mongodb(db_config)

    if db is not None:
        setup_collections(db)
