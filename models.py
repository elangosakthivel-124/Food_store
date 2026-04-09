from sqlalchemy import Column, Integer, String, Float
from database import Base

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
