from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from typing import List
from sqlalchemy.orm import Mapped, relationship, mapped_column
from database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    balance = Column(Float, default=0.0)
    expense_list: Mapped[List["Expense"]] = relationship()

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    amount = Column(Float, default=0.0)
    payer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


