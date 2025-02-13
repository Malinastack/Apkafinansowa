from sqlmodel import Field, SQLModel, Relationship

class UserBase(SQLModel):
    name: str
    balance: float = Field(default=0.0)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()
    expense: list["Expense"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: str | None = None
    balance: float | None = None
    password: str | None = None
    
class ExpenseBase(SQLModel):
    name: str
    amount: float = Field(default=0.0)
    user_id: int | None = Field(default=None, foreign_key="user.id")

class Expense(ExpenseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user: User | None = Relationship(back_populates="expense")

class ExpenseCreate(ExpenseBase):
    pass

class ExpensePublic(ExpenseBase):
    id: int

class ExpenseUpdate(SQLModel):
    name: str | None = None
    amount: float | None = None
    user_id: int | None = None


