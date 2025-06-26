from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Async FastAPI Processor"
    log_level: str = "INFO"
    cat_api_url: str = "https://catfact.ninja/fact"
    redis_host: str = "redis"
    redis_port: int = 6379

    class Config:
        env_file = ".env"

settings = Settings()