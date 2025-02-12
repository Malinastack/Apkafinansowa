from fastapi import FastAPI, HTTPException, Depends
from database import engine
from sqlmodel import Session, SQLModel, select
from models import User, Expense, UserCreate, UserPublic

app = FastAPI()

SQLModel.metadata.create_all(engine)

@app.get("/")
def root():
    return "Siemanko"

@app.post("/create_user", response_model=UserPublic)
async def create_user(user: UserCreate):
    with Session(engine) as session:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

@app.post("/create_expense")
async def create_expense(expense: Expense):
    with Session(engine) as session:
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense
    

@app.get("/get_users", response_model=list[UserPublic])
async def get_users():
    with Session(engine) as session:
        results = session.exec(select(User)).all()
        return results
    
@app.get("/users/{user_id}", response_model=UserPublic)
async def get_user(user_id:int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
        

