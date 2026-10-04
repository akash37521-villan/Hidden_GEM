# Hidden_GEM
Hidden Solan is a full-stack web app connecting travelers with local guides to discover offbeat gems within a 100 km radius of Solan. Built using Python, Django REST Framework, PostgreSQL, and PostGIS for spatial queries, it features interactive Leaflet.js mapping, Docker containerization, and a clean, responsive, framework-free frontend design.


## Running locally

```bash
cd hidden-gem-api
cp .env.example .env        # then fill in SECRET_KEY and DB_PASSWORD
docker compose up --build   # API on http://localhost:8000
python manage.py createsuperuser   # run inside the web container to get an admin
```

Open `hidden-gem-frontend/index.html` (or serve it with `python -m http.server`) and set
`API_BASE_URL` in `hidden-gem-frontend/config.js` to your API address.

## Security

- **Secrets** live in environment variables only (`.env` is git-ignored; see `.env.example`). The app refuses to start in production without a `SECRET_KEY`.
- **Authentication:** token login (`/api/auth/login/`) with password validators (min. 10 characters, common/numeric/similarity checks). HTTP Basic auth is disabled.
- **Authorization:** public sign-up always creates a *tourist*. Only an admin can promote an account to *local guide*, and guides can edit only their own locations.
- **Rate limiting:** login 10/min, registration 5/hour, anonymous API 120/min (DRF throttling).
- **Input validation:** coordinates and radius are range- and NaN-checked; image URLs must be http(s).
- **Transport and headers:** HTTPS redirect, secure cookies, HSTS, `nosniff`, `X-Frame-Options: DENY`, strict CORS allow-list, and a Content-Security-Policy on the frontend.
- **XSS:** all API data is HTML-escaped before rendering; no inline event handlers.
- **Logging:** registrations and failed logins are written to a `security` log.
- **Container:** runs as a non-root user with gunicorn; the database port is bound to localhost in development.
