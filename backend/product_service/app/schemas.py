from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1024)
    price: float = Field(..., gt=0)
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1024)
    price: float | None = Field(default=None, gt=0)
    is_active: bool | None = None


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
