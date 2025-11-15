from fastapi.testclient import TestClient
from app.main import app
from app.config import settings


client = TestClient(app)


def _headers():
    return {"X-API-Key": settings.internal_api_key, "Content-Type": "application/vnd.api+json"}


def test_get_inventory_product_not_found(monkeypatch):
    # Force product client to behave as not found without calling external service
    from app.core import product_client

    async def fake_ensure(product_id: int):
        return product_client.jsonapi_error(
            status=404,
            title="Product not found",
            detail=f"Product with id {product_id} not found",
            pointer="/data/relationships/product",
        )

    monkeypatch.setattr(product_client, "ensure_product_exists", fake_ensure)

    resp = client.get("/api/v1/inventory/123", headers=_headers())
    assert resp.status_code == 404
    assert "errors" in resp.json()


def test_purchase_insufficient_inventory(monkeypatch):
    from app.core.inventory_store import inventory_store
    from app.core import product_client

    async def ok_ensure(product_id: int):
        return None

    monkeypatch.setattr(product_client, "ensure_product_exists", ok_ensure)
    inventory_store.set_quantity(1, 2)

    payload = {
        "data": {
            "type": "purchases",
            "attributes": {"quantity": 5},
        }
    }

    resp = client.post("/api/v1/inventory/1/purchase", json=payload, headers=_headers())
    assert resp.status_code == 400
    body = resp.json()
    assert body["errors"][0]["title"] == "Invalid purchase"
