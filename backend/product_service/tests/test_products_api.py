from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.db import init_db


client = TestClient(app)


def _headers():
    return {"X-API-Key": settings.internal_api_key, "Content-Type": "application/vnd.api+json"}


def setup_module(_module):
    init_db()


def test_create_and_get_product():
    payload = {
        "data": {
            "type": "products",
            "attributes": {
                "name": "Test Product",
                "description": "A product for testing",
                "price": 9.99,
                "is_active": True,
            },
        }
    }
    response = client.post("/api/v1/products", json=payload, headers=_headers())
    assert response.status_code == 201
    body = response.json()
    product_id = body["data"]["id"]

    get_resp = client.get(f"/api/v1/products/{product_id}", headers=_headers())
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["attributes"]["name"] == "Test Product"


def test_update_product():
    payload = {
        "data": {
            "type": "products",
            "attributes": {
                "name": "Product To Update",
                "description": "Old desc",
                "price": 5.0,
                "is_active": True,
            },
        }
    }
    response = client.post("/api/v1/products", json=payload, headers=_headers())
    assert response.status_code == 201
    product_id = response.json()["data"]["id"]

    update_payload = {
        "data": {
            "type": "products",
            "attributes": {
                "description": "New desc",
                "price": 7.5,
            },
        }
    }
    upd_resp = client.patch(f"/api/v1/products/{product_id}", json=update_payload, headers=_headers())
    assert upd_resp.status_code == 200
    assert upd_resp.json()["data"]["attributes"]["description"] == "New desc"


def test_get_product_not_found():
    resp = client.get("/api/v1/products/999999", headers=_headers())
    assert resp.status_code == 404
    body = resp.json()
    assert "errors" in body
