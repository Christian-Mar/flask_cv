# CV-website: architectuur

Flask (server-side rendering met Jinja2) + MongoDB, met de BootstrapMade-template **Craftivo** als frontend.

## 1. Doel
Een persoonlijk online cv/portfolio. De inhoud (profiel, ervaring, opleiding, vaardigheden, projecten, contact) staat in MongoDB en wordt via Flask in de Craftivo-layout getoond. Een beveiligd admin-gedeelte beheert de data.

## 2. Stack
| Laag | Keuze |
|---|---|
| Backend | Python 3.12, Flask (application factory + blueprints) |
| Database | MongoDB, via `pymongo` (optioneel later `flask-pymongo`/`mongoengine`) |
| Frontend | Jinja2-templates, Craftivo (Bootstrap 5, AOS, Swiper, GLightbox, Isotope) |
| Formulieren | Flask-WTF (CSRF + validatie) |
| Auth (admin) | Flask-Login, wachtwoord-hash met `werkzeug.security` |
| Config | `.env` + `python-dotenv` |
| Productie | gunicorn + nginx, MongoDB Atlas of Docker-container |

## 3. Mapstructuur
```
flask_cv_app/
├── app/
│   ├── __init__.py          # create_app(): config, db, blueprints
│   ├── config.py            # Dev/Prod config (MONGO_URI, SECRET_KEY)
│   ├── extensions.py        # mongo client, login manager, csrf
│   ├── blueprints/
│   │   ├── public/          # publieke cv-pagina
│   │   │   ├── routes.py    # GET /, /projecten/<slug>, POST /contact
│   │   │   └── forms.py     # ContactForm
│   │   └── admin/           # beheer (login vereist)
│   │       ├── routes.py    # CRUD per sectie
│   │       └── forms.py
│   ├── models/              # dunne datalaag per collectie
│   │   ├── profile.py
│   │   ├── experience.py
│   │   ├── education.py
│   │   ├── skill.py
│   │   ├── project.py
│   │   └── message.py
│   ├── services/            # logica tussen routes en models
│   │   └── cv_service.py    # stelt de volledige cv-context samen
│   ├── templates/
│   │   ├── base.html        # head, header/nav, footer, scripts (Craftivo)
│   │   ├── public/
│   │   │   ├── index.html   # one-pager met sections
│   │   │   └── sections/    # _hero, _about, _resume, _skills,
│   │   │                    # _portfolio, _contact (partials)
│   │   └── admin/           # login, dashboard, edit-formulieren
│   └── static/
│       └── assets/          # css/ js/ img/ vendor/ van Craftivo
├── scripts/
│   └── seed.py              # vult MongoDB met voorbeeld-cv
├── tests/
├── .env.example
├── requirements.txt
├── wsgi.py                  # entrypoint voor gunicorn
└── ARCHITECTURE.md
```

## 4. Datamodel (MongoDB-collecties)
- **profile** (1 document): `name, title, tagline, bio, photo, email, phone, location, social{linkedin, github, ...}`
- **experience**: `company, role, start, end, description[], order`
- **education**: `school, degree, start, end, description, order`
- **skills**: `name, category, level (0-100), order`
- **projects**: `title, slug, summary, description, images[], tags[], url, featured, order`
- **messages**: `name, email, subject, body, created_at, read` (contactformulier)
- **users**: `username, password_hash` (alleen admin)

Indexen: `projects.slug` (unique), `users.username` (unique), `order` op lijstcollecties.

## 5. Request flow
```
Browser → Flask route (public.index)
        → cv_service.get_cv()      # leest alle collecties
        → render_template("public/index.html", cv=...)
        → Jinja2 vult Craftivo-sections met data
```
Contactformulier: `POST /contact` → validatie (WTF) → opslaan in `messages` → flash-melding.
Admin: `/admin/login` → sessie → CRUD-formulieren per collectie → schrijft naar MongoDB.

## 6. Mapping Craftivo-template → app
| Template-sectie | Partial | Bron |
|---|---|---|
| Hero | `_hero.html` | profile |
| About | `_about.html` | profile |
| Resume | `_resume.html` | experience, education |
| Skills | `_skills.html` | skills |
| Portfolio | `_portfolio.html` | projects |
| Contact | `_contact.html` | profile + messages (form) |

De statische bestanden van de template komen ongewijzigd in `static/assets/`; de HTML wordt opgesplitst in `base.html` + partials en verwijst via `url_for('static', ...)`.

## 7. Routes
| Route | Doel |
|---|---|
| `GET /` | cv one-pager |
| `GET /projecten/<slug>` | projectdetail |
| `POST /contact` | contactbericht opslaan |
| `GET/POST /admin/login`, `/admin/logout` | authenticatie |
| `/admin/<sectie>` (list/new/edit/delete) | beheer per collectie |

## 8. Beveiliging
- `SECRET_KEY` en `MONGO_URI` alleen via omgevingsvariabelen.
- CSRF op alle formulieren; admin-routes achter `@login_required`.
- Jinja2 autoescaping aan; uploads beperken op type/grootte.
- Rate limiting op `/contact` (bijv. Flask-Limiter).

## 9. Bouwvolgorde
1. Project opzetten: venv, `requirements.txt`, application factory, MongoDB-verbinding.
2. Craftivo downloaden, assets plaatsen, `base.html` + partials maken met statische tekst.
3. Datamodellen + `seed.py`; partials koppelen aan data.
4. Contactformulier.
5. Admin (login + CRUD).
6. Tests, Dockerfile/compose, deployment.

## 10. Open keuzes
- Eén taal of meertalig (NL/EN)? Dan een `lang`-veld of aparte documenten per taal.
- PDF-export van het cv (bijv. WeasyPrint)?
- Admin-UI nodig, of volstaat `seed.py`/JSON-import voor een persoonlijk cv?
