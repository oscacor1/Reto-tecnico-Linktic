from pydantic import BaseModel, Field


class InventoryBase(BaseModel):
    product_id: int = Field(..., gt=0)


class InventorySetQuantity(InventoryBase):
    quantity: int = Field(..., ge=0)


class PurchaseRequest(BaseModel):
    quantity: int = Field(..., gt=0)
