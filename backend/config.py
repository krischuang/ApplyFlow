from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./applyflow.db"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"
    resume_storage_path: str = "./resumes"
    seek_max_jobs_per_run: int = 20

    class Config:
        env_file = ".env"


settings = Settings()
