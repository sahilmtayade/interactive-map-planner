from typing import Annotated

from fastapi import Depends, HTTPException

from app.dataaccess.places_repo import PlaceRepoDep, PlaceRepository
from app.models.domain import Place


class PlaceManager:
    def __init__(self, repo: PlaceRepository):
        self.repo = repo

    def get_itinerary(self, country: str) -> list[Place]:
        # Business Rule: Formatting
        return self.repo.get_by_country(country.capitalize())

    def add_place(self, place: Place) -> Place:
        # Business Rule: Validation/Cleanup
        place.name = place.name.strip()
        return self.repo.add(place)

    def remove_place(self, place_id: int):
        if not self.repo.delete(place_id):
            raise HTTPException(status_code=404, detail="Place not found")
        return {"ok": True}


# --- PROVIDER ---
def get_place_mgr(repo: PlaceRepoDep) -> PlaceManager:
    return PlaceManager(repo)


# --- DEPENDENCY ALIAS ---
PlaceManagerDep = Annotated[PlaceManager, Depends(get_place_mgr)]
