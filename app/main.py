import datetime
import os
from typing import Optional
import uuid

from fastapi import Depends, FastAPI
from sqlalchemy import func
from sqlmodel import create_engine, Field, select, Session, SQLModel

app = FastAPI(docs_url=None, redoc_url=None)

database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
# DATABASE_URL uses postgres:// but SQLAlchemy only accepts postgresql://
database_url = database_url.replace("postgres://", "postgresql://")
engine = create_engine(database_url)


class LadyRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lady_id: int
    user_id: uuid.UUID
    timestamp: datetime.datetime


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/statistics")
def get_statistics(*, session: Session = Depends(get_session)):
    lady_counts = {}
    total_count = 0

    for lady_id in range(9):
        statement = select(func.count(LadyRecord.id)).where(LadyRecord.lady_id == lady_id)
        lady_counts[lady_id] = session.exec(statement).first()
        total_count += lady_counts[lady_id]

    lady_statistics = {}
    for lady_id in range(9):
        lady_statistics[str(lady_id)] = (
            round(lady_counts[lady_id] / total_count, 3) if total_count else 0)
    return lady_statistics


@app.post("/statistics", status_code=201)
def save_statistics(*, session: Session = Depends(get_session), lady_record: LadyRecord):
    lady_record.timestamp = datetime.datetime.utcnow()
    session.add(lady_record)
    session.commit()
    return {}
