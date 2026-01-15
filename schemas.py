from pydantic import BaseModel

class FoodCreate(BaseModel):
    name: str
    category: str
    price: float

class FoodResponse(FoodCreate):
    id: int

    class Config:
        from_attributes = True
