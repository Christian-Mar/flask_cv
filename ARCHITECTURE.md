# CV-website: architectuur

Flask (server-side rendering met Jinja2) met de BootstrapMade-template **Craftivo** als frontend. De cv-inhoud staat in één JSON-bestand; er is geen database.

## 1. Stack
| Laag | Keuze |
|---|---|
| Omgeving | Python 3.12, uv (`pyproject.toml`, `uv.lock`) |
| Backend | Flask, application factory + blueprint |
| Data | `data/cv.json` (cv), `data/messages.jsonl` (contactberichten) |
| Frontend | Jinja2, Craftivo (Bootstrap 5, AOS, Typed.js, GLightbox, Isotope) |
| Formulieren | Flask-WTF (CSRF + validatie), email-validator |
| Productie | gunicorn (`wsgi.py`) |

## 2. Mapstructuur
```
flask_cv_app/
├── app/
│   ├── __init__.py          # create_app()
│   ├── config.py            # SECRET_KEY, CV_FILE, MESSAGES_FILE
│   ├── extensions.py        # CSRF
│   ├── blueprints/public/   # routes.py (/, /contact), forms.py
│   ├── services/cv_service.py   # get_cv() leest JSON, save_message()
│   ├── templates/
│   │   ├── base.html
│   │   └── public/          # index.html, _header/_footer/_social, sections/_*.html
│   └── static/assets/       # Craftivo css, js, img, vendor
├── data/
│   ├── cv.json              # JOUW CV-GEGEVENS
│   └── messages.jsonl       # ontvangen berichten (niet in git)
├── pyproject.toml, uv.lock
├── wsgi.py
└── .env                     # SECRET_KEY
```

## 3. Dataformaat (`data/cv.json`)
- **profile**: `name, title, roles[], tagline, headline, bio[], photo, hero_image, email, phone, location, address, degree, experience_label, availability, cv_url, stats[{value,label}], social{linkedin,github,x,instagram,facebook}`
- **experience[]**: `role, company, period, current, icon, description, tags[]` (volgorde = volgorde in bestand)
- **education[]**: `degree, school, level, period, description, achievement, icon, certs[{name,year}]`
- **skills[]**: `name, level (0-100)`
- **projects[]**: `slug, title, category, tags[], year, image, summary, url`

Afbeeldingspaden zijn relatief aan `app/static/assets/img/`. Lege velden worden niet getoond.

## 4. Request flow
- `GET /` → `get_cv()` leest `cv.json` → `index.html` vult de Craftivo-sections. Wijzigingen in het JSON zijn direct zichtbaar (geen herstart nodig).
- `POST /contact` → ContactForm (CSRF + validatie) → regel toevoegen aan `messages.jsonl` → antwoord "OK" voor `validate.js`.

## 5. Template → partial
Hero, About (incl. skills), Resume (experience + education), Portfolio, Contact. De Services-sectie van Craftivo is weggelaten.

## 6. Later (optioneel)
Projectdetailpagina's, meertaligheid, PDF-export, deployment (gunicorn + nginx).
