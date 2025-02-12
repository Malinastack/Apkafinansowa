from sqlmodel import Field, Session, SQLModel, create_engine, select

DATABASE_URL = "postgresql://postgres:siemanko@localhost/postgres"

engine = create_engine(DATABASE_URL, echo=True)


