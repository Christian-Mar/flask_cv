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
│   │   ├── base.html        # head, CSS/JS, {% block content %}
│   │   ├── components/      # herbruikbare macro's (zie §5)
│   │   │   ├── layout.html, about.html, resume.html
│   │   │   └── portfolio.html, contact.html
│   │   └── public/          # index.html, _header.html, _footer.html
│   │       └── sections/    # _hero, _about, _resume, _portfolio, _contact
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
- **skills[]**: `name, level (0-100, optioneel)`
- **languages[]**: `name, label`
- **projects[]**: `slug, title, category, tags[], year, image, summary, url`

Afbeeldingspaden zijn relatief aan `app/static/assets/img/`. Lege velden worden niet getoond.

## 4. Request flow
- `GET /` → `get_cv()` leest `cv.json` → `index.html` vult de Craftivo-sections. Wijzigingen in het JSON zijn direct zichtbaar (geen herstart nodig).
- `POST /contact` → ContactForm (CSRF + validatie) → regel toevoegen aan `messages.jsonl` → antwoord "OK" voor `validate.js`.

## 5. Templates en componenten
Pagina's bestaan uit drie lagen: `base.html` → secties (`public/sections/`) → componenten (`components/`, Jinja-macro's). Een sectie bevat de indeling en roept componenten aan; de details staan in de componenten. Macro's zien `cv` niet vanzelf: data wordt als parameter meegegeven (`profile_card(cv.profile)`). Importeren: `{% from "components/x.html" import naam %}`.

```
base.html
├─ public/_header.html ........ nav_item
├─ public/index.html
│  ├─ sections/_hero.html ..... social_links
│  ├─ sections/_about.html .... section_title
│  │     profile_card (stat_item, social_links) · details_grid (detail_item)
│  │     skills_block (skill_bar | skill_tag) · languages_block (language_item)
│  ├─ sections/_resume.html ... section_title · column_header
│  │     exp_card · timeline_item (cert_item)
│  ├─ sections/_portfolio.html  section_title · filters · portfolio_card
│  └─ sections/_contact.html .. section_title · info_item · contact_form
└─ public/_footer.html ........ social_links, nav_item
```

| Componentbestand | Macro's |
|---|---|
| `layout.html` | `section_title`, `social_links`, `nav_item` |
| `about.html` | `profile_card`, `stat_item`, `details_grid`, `detail_item`, `skills_block`, `skill_bar`, `skill_tag`, `languages_block`, `language_item` |
| `resume.html` | `column_header`, `exp_card`, `timeline_item`, `cert_item` |
| `portfolio.html` | `filters`, `portfolio_card` |
| `contact.html` | `info_item`, `contact_form` |

Nieuwe sectie toevoegen: maak `sections/_naam.html`, voeg een `include` toe in `index.html` en een `nav_item` in `_header.html`. Data erin tonen: lijst toevoegen aan `cv.json` en doorgeven in `cv_service.get_cv()`.

Aandachtspunten: de Services-sectie van Craftivo is weggelaten. Skills zonder `level` tonen als tags (geen percentage); `languages` heeft een eigen blok; `projects` leeg verbergt de portfoliosectie en het menu-item.

## 6. Later (optioneel)
Projectdetailpagina's, meertaligheid, PDF-export, deployment (gunicorn + nginx).
