from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, select

from app.models.domain import Place
from app.services.database import DatabaseService, DbServiceDep


class PlaceRepository:
    def __init__(self, db_service: DatabaseService):
        self.session_maker = db_service.get_session

    def get_by_country(self, country: str) -> list[Place]:
        session: Session = next(self.session_maker())
        statement = select(Place).where(Place.country == country)
        return list(session.exec(statement).all())

    def add(self, place: Place) -> Place:
        session: Session = next(self.session_maker())
        session.add(place)
        session.commit()
        session.refresh(place)
        return place

    def delete(self, place_id: int) -> bool:
        session: Session = next(self.session_maker())
        place = session.get(Place, place_id)
        if place:
            session.delete(place)
            session.commit()
            return True
        return False


# --- PROVIDER ---
def get_place_repo(db_service: DbServiceDep) -> PlaceRepository:
    return PlaceRepository(db_service)


# --- DEPENDENCY ALIAS ---
PlaceRepoDep = Annotated[PlaceRepository, Depends(get_place_repo)]
