import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    CV_FILE = Path(os.environ.get("CV_FILE", BASE_DIR / "data" / "cv.json"))
    MESSAGES_FILE = Path(os.environ.get("MESSAGES_FILE", BASE_DIR / "data" / "messages.jsonl"))
