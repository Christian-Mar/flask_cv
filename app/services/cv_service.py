import json
import re
from datetime import datetime, timezone

from flask import current_app


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def get_cv() -> dict:
    """Leest data/cv.json en stelt de cv-context voor de templates samen."""
    with open(current_app.config["CV_FILE"], encoding="utf-8") as f:
        data = json.load(f)

    profile = data.get("profile", {})
    profile.setdefault("social", {})
    profile.setdefault("roles", [])
    profile.setdefault("bio", [])

    projects = data.get("projects", [])
    categories: dict[str, str] = {}
    for p in projects:
        p["filter"] = _slug(p["category"])
        categories.setdefault(p["filter"], p["category"])

    return {
        "profile": profile,
        "experience": data.get("experience", []),
        "education": data.get("education", []),
        "skills": data.get("skills", []),
        "projects": projects,
        "categories": list(categories.items()),
    }


def save_message(name: str, email: str, subject: str, body: str) -> None:
    """Voegt een contactbericht toe aan data/messages.jsonl (één JSON-regel per bericht)."""
    record = {
        "name": name,
        "email": email,
        "subject": subject,
        "body": body,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    path = current_app.config["MESSAGES_FILE"]
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
