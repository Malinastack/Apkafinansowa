from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Annotated
import models
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session


app = FastAPI()

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name:str
    balance: float
    expense_list: list = Field(default=[])

class ExpenseCreate(BaseModel):
    amount: float
    name: str
    payer_id: int


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def root():
    return "Siemanko"

@app.post("/create_user")
async def create_user(user: UserCreate, db: db_dependency):
    db_user = models.Users(name = user.name, balance = user.balance)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

@app.post("/create_expense")
async def create_expense(expense: ExpenseCreate, db: db_dependency):
    db_expense = models.Expense(name = expense.name, amount = expense.amount, payer_id = expense.payer_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

