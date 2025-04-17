from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from typing import Annotated
from ..utils import from_env

def include_routers(app, routers):
    for router in routers:
        app.include_router(router=router)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

allowed_origins = [
    #
]
DB_URL = from_env('DB_URL')
connect_args = {"check_same_thread": False}
engine = create_engine(DB_URL, connect_args=connect_args)
SessionDep = Annotated[Session, Depends(get_session)]