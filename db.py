import os
from pymongo import MongoClient


def get_client():
    """Return a MongoClient. Reads MONGODB_URI from env or defaults to localhost."""
    uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    # short timeout so failures surface quickly in dev
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    # validate connection now
    client.server_info()
    return client


def get_db(db_name: str | None = None):
    """Return a database. Reads MONGODB_DB from env or uses 'expense_tracker'."""
    client = get_client()
    if db_name is None:
        db_name = os.environ.get("MONGODB_DB", "expense_tracker")
    return client[db_name]


def close_client(client: MongoClient):
    try:
        client.close()
    except Exception:
        pass


def init_db(db_name: str | None = None):
    """Return a database and ensure basic indexes exist (idempotent).

    Safe to call at startup; if Mongo isn't reachable this will raise.
    """
    mongodb = get_db(db_name)
    try:
        # ensure a unique index on member name
        mongodb.get_collection("members").create_index("name", unique=True)
    except Exception:
        # ignore index creation errors (e.g., permissions) to avoid crashing the app
        pass
    try:
        # index category for faster lookups/updates
        mongodb.get_collection("expenses").create_index("category")
    except Exception:
        pass
    return mongodb
