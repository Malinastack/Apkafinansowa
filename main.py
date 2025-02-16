from fastapi import FastAPI, HTTPException, Depends, Query
from database import engine
from sqlmodel import Session, SQLModel, select
from models import User, Expense, UserCreate, UserPublic, UserUpdate, ExpenseCreate, ExpensePublic, ExpenseUpdate, ExpensePublicWithUser, UserPublicWithExpenses

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

SQLModel.metadata.create_all(engine)

def hash_password(password: str) -> str:
    # Use something like passlib here
    return f"not really hashed {password} hehehe"

@app.get("/")
def root():
    return "Siemanko"

@app.post("/create_user", response_model=UserPublic)
async def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    hashed_password = hash_password(user.password)
    extra_data = {"hashed_password": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users", response_model=list[UserPublic])
async def get_users(*, session: Session = Depends(get_session)):
    results = session.exec(select(User)).all()
    return results
    
@app.get("/users/{user_id}", response_model=UserPublicWithExpenses)
async def get_user(*, session: Session = Depends(get_session), user_id:int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    
@app.patch("/users/{user_id}", response_model=UserPublic)
async def update_user(*, session: Session = Depends(get_session), user_id: int, user: UserUpdate):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = hash_password(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete("/users/{user.id}")
async def delete_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"User deleted": True}

@app.post("/create_expense", response_model=ExpensePublic)
async def create_expense(*, session: Session = Depends(get_session), expense: ExpenseCreate):
    db_expense = Expense.model_validate(expense)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense

@app.get("/expenses", response_model= list[ExpensePublic])
async def get_expenses(*, session: Session = Depends(get_session)):
    result = session.exec(select(Expense)).all()
    return result

@app.get("/expenses/{expense_id}", response_model=ExpensePublicWithUser)
async def get_expense(*, session: Session = Depends(get_session), expense_id: int):
    db_expense = session.get(Expense, expense_id)
    if not db_expense:
        return HTTPException(status_code=404, detail="Expense not found")
    return db_expense
    
@app.patch("/expense/{expense_id}", response_model=ExpensePublic)
async def update_expense(*, session: Session = Depends(get_session), expense_id: int, expense: ExpenseUpdate):
    db_expense = session.get(Expense, expense_id)
    if not db_expense:
        return HTTPException(status_code=404, detail="Expense not found")
    expense_data = expense.model_dump(exclude_unset=True)
    for key, value in expense_data.items():
        setattr(db_expense, key, value)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense

@app.delete("/expense/{expense_id}")
async def delete_expense(*, session: Session = Depends(get_session), expense_id: int):
    db_expense = session.get(Expense, expense_id)
    if not db_expense:
        return HTTPException(status_code=404, detail="Expense not found")
    session.delete(db_expense)
    session.commit()
    return {"Expense deleted": True}




        

