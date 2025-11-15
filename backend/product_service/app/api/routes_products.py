from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db, verify_api_key
from ..core.jsonapi import JSONAPIResponse, jsonapi_single, jsonapi_list, jsonapi_error


router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(verify_api_key)],
)


@router.post(
    "",
    response_class=JSONAPIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a product",
)
def create_product(payload: dict, db: Session = Depends(get_db)):
    attributes = payload.get("data", {}).get("attributes", {})
    product_in = schemas.ProductCreate(**attributes)
    product = models.Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return JSONAPIResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonapi_single(
            "products",
            product.id,
            schemas.ProductOut.model_validate(product).model_dump(),
        ),
    )


@router.get(
    "/{product_id}",
    response_class=JSONAPIResponse,
    summary="Get a product by id",
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(models.Product, product_id)
    if not product:
        return jsonapi_error(
            status=status.HTTP_404_NOT_FOUND,
            title="Product not found",
            detail=f"Product with id {product_id} not found",
            pointer="/data",
        )
    return JSONAPIResponse(
        content=jsonapi_single(
            "products",
            product.id,
            schemas.ProductOut.model_validate(product).model_dump(),
        )
    )


@router.patch(
    "/{product_id}",
    response_class=JSONAPIResponse,
    summary="Update a product by id",
)
def update_product(product_id: int, payload: dict, db: Session = Depends(get_db)):
    product = db.get(models.Product, product_id)
    if not product:
        return jsonapi_error(
            status=status.HTTP_404_NOT_FOUND,
            title="Product not found",
            detail=f"Product with id {product_id} not found",
            pointer="/data",
        )
    attributes = payload.get("data", {}).get("attributes", {})
    update_in = schemas.ProductUpdate(**attributes)
    for field, value in update_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return JSONAPIResponse(
        content=jsonapi_single(
            "products",
            product.id,
            schemas.ProductOut.model_validate(product).model_dump(),
        )
    )


@router.delete(
    "/{product_id}",
    response_class=JSONAPIResponse,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product by id",
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(models.Product, product_id)
    if not product:
        return jsonapi_error(
            status=status.HTTP_404_NOT_FOUND,
            title="Product not found",
            detail=f"Product with id {product_id} not found",
            pointer="/data",
        )
    db.delete(product)
    db.commit()
    return JSONAPIResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


@router.get(
    "",
    response_class=JSONAPIResponse,
    summary="List products with pagination",
)
def list_products(
    db: Session = Depends(get_db),
    page_number: int = Query(1, alias="page[number]", ge=1),
    page_size: int = Query(10, alias="page[size]", ge=1, le=100),
):
    total = db.query(models.Product).count()
    items = (
        db.query(models.Product)
        .offset((page_number - 1) * page_size)
        .limit(page_size)
        .all()
    )
    payload_items = [
        {
            "id": product.id,
            "attributes": schemas.ProductOut.model_validate(product).model_dump(),
        }
        for product in items
    ]
    meta = {
        "total": total,
        "page": page_number,
        "size": page_size,
    }
    return JSONAPIResponse(content=jsonapi_list("products", payload_items, meta=meta))
