from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "Product Service"
    api_v1_prefix: str = "/api/v1"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./products.db")
    internal_api_key: str = os.getenv("INTERNAL_API_KEY", "super-secret-key")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
