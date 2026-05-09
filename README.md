# ApplyFlow

AI-powered auto-apply system for Australian software engineering jobs.

## How it works

1. Upload your PDF resume — Claude AI parses it into a structured profile
2. Set preferences: AU city, salary range, tech stack, match score threshold
3. Hit **Start Run** — the system:
   - Scrapes Seek.com.au for software engineer roles
   - Scores each job against your profile using Claude AI (0–100)
   - Auto-fills and submits Quick Apply forms via Playwright browser automation
4. Track every application in the dashboard

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12 + FastAPI |
| Frontend | Next.js 14 (App Router) + Tailwind CSS |
| Database | SQLite (dev) / PostgreSQL (prod) |
| ORM | SQLAlchemy 2.0 |
| AI | Anthropic Claude API |
| Browser Automation | Playwright (Python) |
| PDF Parsing | pypdf |
| Container | Docker + Docker Compose |

## Project Structure

```
ApplyFlow/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Settings from .env
│   ├── database.py          # SQLAlchemy engine + session
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic v2 request/response schemas
│   ├── routers/             # API route handlers
│   └── services/
│       ├── claude_service.py          # Claude AI calls
│       ├── resume_parser.py           # PDF to structured profile
│       ├── seek_scraper.py            # Playwright Seek.com.au scraper
│       ├── seek_applier.py            # Playwright form submission
│       └── auto_apply_orchestrator.py # End-to-end orchestration
└── frontend/
    ├── app/                 # Next.js App Router pages
    │   ├── page.tsx         # Dashboard
    │   ├── profile/         # Resume upload + profile editor
    │   ├── preferences/     # Job search preferences
    │   ├── auto-apply/      # Trigger runs + live status
    │   └── applications/    # View all tracked applications
    ├── components/          # Navbar, StatusBadge
    └── lib/api.ts           # Typed API client
```

## Local Development

### Prerequisites

- Python 3.12+
- Node.js 20+
- An [Anthropic API key](https://console.anthropic.com/)

### Backend

```bash
cd backend
cp .env.example .env        # add ANTHROPIC_API_KEY
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
uvicorn main:app --reload
```

API runs at **http://localhost:8000** · Swagger docs at **http://localhost:8000/docs**

### Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

UI runs at **http://localhost:3000**

## Docker (full stack)

```bash
cp backend/.env.example .env
# Edit .env and set ANTHROPIC_API_KEY=sk-ant-...
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/profile/resume` | Upload PDF resume (AI parses it) |
| GET / PUT | `/api/v1/profile` | View / update profile |
| GET / PUT | `/api/v1/profile/preferences` | Job search preferences |
| POST | `/api/v1/auto-apply/run` | Start an auto-apply run |
| GET | `/api/v1/auto-apply/runs/{id}` | Poll run status |
| GET | `/api/v1/applications` | List all tracked applications |
| PATCH | `/api/v1/applications/{id}/status` | Update application status |

## Notes

- **Seek selectors may drift.** If scraping breaks, update `data-automation` selectors in `backend/services/seek_scraper.py` and `seek_applier.py`.
- **Seek Quick Apply only.** Jobs that redirect to a company website are skipped in this MVP.
- This is a single-user system. Multi-user auth is planned for a future version.
