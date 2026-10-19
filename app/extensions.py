from flask_login import LoginManager
from flask_wtf import CSRFProtect
from pymongo import MongoClient
from pymongo.database import Database

csrf = CSRFProtect()
login_manager = LoginManager()

_client: MongoClient | None = None


def init_mongo(app) -> None:
    global _client
    _client = MongoClient(app.config["MONGO_URI"])


def get_db() -> Database:
    from flask import current_app

    return _client[current_app.config["MONGO_DB_NAME"]]


@login_manager.user_loader
def load_user(user_id: str):
    # Placeholder: wordt vervangen zodra het users-model bestaat.
    return None
