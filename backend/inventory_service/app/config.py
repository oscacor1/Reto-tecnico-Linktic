from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "Inventory Service"
    api_v1_prefix: str = "/api/v1"
    internal_api_key: str = os.getenv("INTERNAL_API_KEY", "super-secret-key")
    product_service_base_url: str = os.getenv(
        "PRODUCT_SERVICE_BASE_URL", "http://product-service:8000"
    )
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "2.0"))
    request_max_retries: int = int(os.getenv("REQUEST_MAX_RETRIES", "3"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
