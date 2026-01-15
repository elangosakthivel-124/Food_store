from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Store API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root
@app.get("/")
def read_root():
    return {"message": "Welcome to Food API"}

# Create food item
@app.post("/foods/", response_model=schemas.FoodResponse)
def create_food(food: schemas.FoodCreate, db: Session = Depends(get_db)):
    db_food = models.Food(
        name=food.name,
        category=food.category,
        price=food.price
    )
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

# Get all food items
@app.get("/foods/", response_model=list[schemas.FoodResponse])
def get_foods(db: Session = Depends(get_db)):
    return db.query(models.Food).all()

# Get food by ID
@app.get("/foods/{food_id}", response_model=schemas.FoodResponse)
def get_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food

# Update food
@app.put("/foods/{food_id}", response_model=schemas.FoodResponse)
def update_food(food_id: int, food: schemas.FoodCreate, db: Session = Depends(get_db)):
    db_food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")

    db_food.name = food.name
    db_food.category = food.category
    db_food.price = food.price

    db.commit()
    db.refresh(db_food)
    return db_food

# Delete food
@app.delete("/foods/{food_id}")
def delete_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    db.delete(food)
    db.commit()
    return {"message": "Food deleted successfully"}
