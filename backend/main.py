from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from database import engine, Base
from routers import applications, profile, auto_apply

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ApplyFlow",
    description="AI auto-apply for Australian software engineering jobs",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(applications.router, prefix="/api/v1/applications", tags=["Applications"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["Profile"])
app.include_router(auto_apply.router, prefix="/api/v1/auto-apply", tags=["Auto Apply"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
