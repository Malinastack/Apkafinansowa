from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    name: str
    balance: float = Field(default=0.0)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int

class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    amount: float = Field(default=0.0)
    payer_id: int

