# flask_cv

Persoonlijke cv-website met Flask en de Craftivo-template. De cv-gegevens staan in `data/cv.json`. Zie [ARCHITECTURE.md](ARCHITECTURE.md) voor de opbouw.

## Starten
```
uv sync
uv run flask --app wsgi run --debug
```

## TODO
- [ ] Cv kunnen downloaden (bijv. als PDF) en de knop "Download cv" in de profielkaart laten werken (`cv_url` in `data/cv.json`).
- [ ] De website mooi kunnen printen: print-CSS (`@media print`) toevoegen, zodat menu, preloader en animaties verdwijnen en de pagina netjes op A4 past.
