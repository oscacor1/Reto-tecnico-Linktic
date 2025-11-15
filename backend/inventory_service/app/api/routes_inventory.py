from fastapi import APIRouter, Depends, status
from ..deps import verify_api_key
from ..schemas import InventorySetQuantity, PurchaseRequest
from ..core.inventory_store import inventory_store
from ..core.jsonapi import JSONAPIResponse, jsonapi_single, jsonapi_error
from ..core.product_client import ensure_product_exists


router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(verify_api_key)],
)


@router.get(
    "/{product_id}",
    response_class=JSONAPIResponse,
    summary="Get inventory quantity for a product",
)
async def get_inventory(product_id: int):
    error_response = await ensure_product_exists(product_id)
    if error_response:
        return error_response
    qty = inventory_store.get_quantity(product_id)
    return JSONAPIResponse(
        content=jsonapi_single(
            "inventories",
            product_id,
            {"product_id": product_id, "quantity": qty},
        )
    )


@router.post(
    "",
    response_class=JSONAPIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Set initial quantity for a product",
)
async def set_inventory(payload: dict):
    attributes = payload.get("data", {}).get("attributes", {})
    body = InventorySetQuantity(**attributes)
    error_response = await ensure_product_exists(body.product_id)
    if error_response:
        return error_response
    inventory_store.set_quantity(body.product_id, body.quantity)
    print(f"[EVENT] Inventory set for product {body.product_id}: {body.quantity}")
    return JSONAPIResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonapi_single(
            "inventories",
            body.product_id,
            {"product_id": body.product_id, "quantity": body.quantity},
        ),
    )


@router.post(
    "/{product_id}/purchase",
    response_class=JSONAPIResponse,
    summary="Decrease quantity after purchase",
)
async def purchase(product_id: int, payload: dict):
    attributes = payload.get("data", {}).get("attributes", {})
    body = PurchaseRequest(**attributes)

    error_response = await ensure_product_exists(product_id)
    if error_response:
        return error_response

    try:
        new_qty = inventory_store.decrease_quantity(product_id, body.quantity)
    except ValueError as exc:
        return jsonapi_error(
            status=400,
            title="Invalid purchase",
            detail=str(exc),
            pointer="/data/attributes/quantity",
        )
    print(f"[EVENT] Inventory changed for product {product_id}: new quantity {new_qty}")
    return JSONAPIResponse(
        content=jsonapi_single(
            "inventories",
            product_id,
            {"product_id": product_id, "quantity": new_qty},
        )
    )
