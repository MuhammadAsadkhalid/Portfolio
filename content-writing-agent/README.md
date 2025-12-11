## Content Writing Assistant

Backend: Flask + Gemini. Frontend: static HTML/JS.

### Local dev
- Install Python 3.11+
- `pip install -r backend/requirements.txt`
- Add `.env` in `backend/` with `GEMINI_API_KEY=<your-key>` and optional `FLASK_DEBUG=True`
- Run `python backend/main.py`
- Open `frontend/index.html` in a browser

### Railway deploy
Railway will read `railway.toml`:
- Build: `pip install -r backend/requirements.txt`
- Start: `cd backend && gunicorn -b 0.0.0.0:$PORT main:app`
- Health: `GET /health`
- Env: `PYTHON_VERSION=3.11`, `FLASK_DEBUG=False`

Steps:
1) `railway init` (if not already)
2) Set secrets: `railway variables set GEMINI_API_KEY=...`
3) Deploy: `railway up`
4) After deploy, update frontend `API_BASE_URL` if using a separate static host. By default it uses same-origin `https://<railway-domain>/api`.

Frontend options on Railway:
- Easiest: add a Static service pointing to `frontend/` (build command empty, output dir `frontend`). It will call the backend via the same-origin URL above.
- Or serve locally via `python -m http.server` during development.
