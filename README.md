# ApplyFlow

**ApplyFlow** doesn't just track job applications — it submits them. It scrapes listings from Seek.com.au, scores each one against your resume with Claude, and drives Playwright through the real Quick Apply form, submit button included.

A Spring Boot (Java) implementation of the same `/api/v1/applications` domain exists as a separate polyglot exercise: [ApplyFlow-Java](https://github.com/krischuang/ApplyFlow-Java). It was originally developed in this repository and was split out since it has no dependency on the Python/Next.js app.

## How it Works

1. **Upload Your Resume**: Claude parses your PDF resume into a structured profile.
2. **Set Preferences**: Define your preferences, including location, salary range, tech stack, and match score threshold.
3. **Start an Auto-Apply Run**: Initiate the system to scrape Seek.com.au for software engineer roles, score each job against your profile using Claude AI (0–100), and auto-fill and submit Quick Apply forms via Playwright browser automation.
4. **Track Your Applications**: Monitor every application in real-time from the dashboard.

## Architecture

**ApplyFlow** is built on a robust architecture that ensures scalability and reliability:

- **Backend**: Developed with Python 3.12 and FastAPI, providing a high-performance API for managing user profiles, job preferences, and auto-apply runs.
- **Frontend**: Built using Next.js 14 (App Router) and Tailwind CSS, offering a modern and intuitive user interface.
- **Database**: Utilizes SQLite in development and PostgreSQL in production for efficient data storage and retrieval.
- **ORM**: SQLAlchemy 2.0 ensures seamless interaction with the database.
- **AI**: Claude AI is used for advanced parsing and scoring of job descriptions against user profiles.
- **Browser Automation**: Playwright handles form submissions on Seek.com.au, ensuring compatibility across different browsers.
- **PDF Parsing**: pypdf library converts PDF resumes into structured data.

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

## Setup Instructions

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

## Docker (Full Stack)

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

## API Workflow

1. **Upload Resume**: Use the `/api/v1/profile/resume` endpoint to upload your PDF resume.
2. **Set Preferences**: Manage your job search preferences using the `/api/v1/profile/preferences` endpoint.
3. **Start Run**: Initiate an auto-apply run with the `/api/v1/auto-apply/run` endpoint.
4. **Track Runs**: Poll the status of runs using the `/api/v1/auto-apply/runs/{id}` endpoint.
5. **List Applications**: Retrieve all tracked applications with the `/api/v1/applications` endpoint.

## Job Filtering Pipeline

**ApplyFlow** employs a two-step filtering pipeline to ensure efficient and accurate job matching:

1. **Cheap Filtering**: Initial filtering based on location, salary range, and tech stack is performed locally.
2. **LLM Scoring**: Advanced scoring using Claude AI ensures that only the most relevant jobs are submitted.

## Testing

```bash
cd backend
pip install -r requirements.txt
python -m pytest
```

10 tests cover the applications CRUD API against an in-memory SQLite database — no real Postgres or Anthropic API key needed to run them.

## Status

Personal project, actively used for my own job search. Not deployed as a hosted service.

## License

MIT — see [LICENSE](LICENSE).
