from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.models.config import AppConfig, ConfigDep


class DatabaseService:
    """Pure Python Class. No FastAPI dependencies in __init__."""

    def __init__(self, config: AppConfig):
        self.engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})

    def get_session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session


# --- PROVIDER ---
def get_db_service(config: ConfigDep) -> DatabaseService:
    return DatabaseService(config)


# --- DEPENDENCY ALIAS ---
DbServiceDep = Annotated[DatabaseService, Depends(get_db_service)]
