import asyncio
import httpx
from .jsonapi import jsonapi_error
from ..config import settings


async def fetch_product(product_id: int) -> dict | None:
    """Calls Product Service with retry and timeout. Returns product attributes dict or None if 404."""
    url = f"{settings.product_service_base_url}/api/v1/products/{product_id}"
    headers = {
        "X-API-Key": settings.internal_api_key,
        "Accept": "application/vnd.api+json",
    }
    timeout = settings.request_timeout_seconds

    for attempt in range(1, settings.request_max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, headers=headers)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json().get("data", {})
            return data.get("attributes", {})
        except (httpx.RequestError, httpx.HTTPStatusError):
            if attempt == settings.request_max_retries:
                raise
            await asyncio.sleep(0.2 * attempt)

    return None


async def ensure_product_exists(product_id: int):
    try:
        product = await fetch_product(product_id)
    except Exception as exc:  # noqa: BLE001
        # communication error with Product service
        return jsonapi_error(
            status=503,
            title="Product service unavailable",
            detail=str(exc),
            pointer="/data/relationships/product",
        )
    if product is None:
        return jsonapi_error(
            status=404,
            title="Product not found",
            detail=f"Product with id {product_id} not found",
            pointer="/data/relationships/product",
        )
    return None
