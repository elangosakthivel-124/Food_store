from pydantic import BaseModel

class FoodBase(BaseModel):
    name: str
    category: str
    price: float

class FoodCreate(FoodBase):
    pass

class FoodResponse(FoodBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 compatible
