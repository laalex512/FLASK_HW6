from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    title: str = Field(max_length=72)
    description: str = Field()
    price: float = Field(ge=0, le=10_000)


class ProductIn(BaseModel):
    title: str = Field(max_length=72)
    description: str = Field()
    price: float = Field(ge=0, le=10_000)
