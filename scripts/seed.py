"""Vult MongoDB met een voorbeeld-cv. Gebruik: uv run python -m scripts.seed"""
from app import create_app
from app.extensions import get_db

PROFILE = {
    "name": "Jouw Naam",
    "title": "Full Stack Developer",
    "roles": ["Developer", "Ontwerper", "Freelancer"],
    "tagline": "Korte introductie over wie je bent en wat je doet.",
    "headline": "Ideeën omzetten in werkende software",
    "bio": [
        "Eerste alinea over jezelf en je achtergrond.",
        "Tweede alinea over waar je goed in bent en wat je zoekt.",
    ],
    "photo": "profile/profile-square-3.webp",
    "hero_image": "profile/profile-bg-5.webp",
    "email": "naam@example.com",
    "phone": "+31 6 12345678",
    "location": "Amsterdam, Nederland",
    "address": "",
    "degree": "Bachelor ICT",
    "experience_label": "8+ jaar",
    "availability": "Beschikbaar",
    "cv_url": "",
    "stats": [
        {"value": "25", "label": "Projecten"},
        {"value": "8+", "label": "Jaren"},
    ],
    "social": {"linkedin": "https://www.linkedin.com/", "github": "https://github.com/"},
}

EXPERIENCE = [
    {"order": 1, "role": "Senior Developer", "company": "Bedrijf A", "period": "2023 - heden", "current": True,
     "icon": "buildings", "description": "Omschrijving van de functie.", "tags": ["Python", "Flask"]},
    {"order": 2, "role": "Developer", "company": "Bedrijf B", "period": "2020 - 2023", "icon": "laptop",
     "description": "Omschrijving van de functie."},
]

EDUCATION = [
    {"order": 1, "period": "2016 - 2020", "level": "Bachelor", "degree": "Bachelor ICT", "school": "Hogeschool X",
     "description": "Korte omschrijving.", "icon": "mortarboard-fill"},
    {"order": 2, "period": "2018 - 2023", "level": "Certificaten", "degree": "Certificeringen", "icon": "patch-check-fill",
     "certs": [{"name": "Certificaat A", "year": "2023"}, {"name": "Certificaat B", "year": "2021"}]},
]

SKILLS = [
    {"order": 1, "name": "Python & Flask", "level": 90},
    {"order": 2, "name": "MongoDB", "level": 80},
    {"order": 3, "name": "HTML & CSS", "level": 85},
]

PROJECTS = [
    {"order": 1, "slug": "project-1", "title": "Project één", "category": "Development", "tags": ["Python", "Flask"],
     "year": "2024", "image": "portfolio/portfolio-1.webp", "summary": "Korte omschrijving.", "url": ""},
    {"order": 2, "slug": "project-2", "title": "Project twee", "category": "Design", "tags": ["UI/UX"],
     "year": "2023", "image": "portfolio/portfolio-2.webp", "summary": "Korte omschrijving.", "url": ""},
]


def main() -> None:
    app = create_app()
    with app.app_context():
        db = get_db()
        db.profile.replace_one({}, PROFILE, upsert=True)
        for name, docs in [("experience", EXPERIENCE), ("education", EDUCATION), ("skills", SKILLS), ("projects", PROJECTS)]:
            db[name].delete_many({})
            db[name].insert_many(docs)
        db.projects.create_index("slug", unique=True)
    print("Seed klaar.")


if __name__ == "__main__":
    main()
