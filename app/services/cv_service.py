import re

from ..extensions import get_db


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def get_cv() -> dict:
    """Stelt de volledige cv-context samen uit alle collecties."""
    db = get_db()
    profile = db.profile.find_one({}, {"_id": 0}) or {}
    profile.setdefault("social", {})
    profile.setdefault("roles", [])
    profile.setdefault("bio", [])

    projects = list(db.projects.find({}, {"_id": 0}).sort("order", 1))
    categories: dict[str, str] = {}
    for p in projects:
        p["filter"] = _slug(p["category"])
        categories.setdefault(p["filter"], p["category"])

    return {
        "profile": profile,
        "experience": list(db.experience.find({}, {"_id": 0}).sort("order", 1)),
        "education": list(db.education.find({}, {"_id": 0}).sort("order", 1)),
        "skills": list(db.skills.find({}, {"_id": 0}).sort("order", 1)),
        "projects": projects,
        "categories": list(categories.items()),
    }
