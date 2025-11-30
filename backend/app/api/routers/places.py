from fastapi import APIRouter

from app.business.places_mgr import PlaceManagerDep
from app.models.domain import Place

router = APIRouter(prefix="/places", tags=["Places"])


@router.get("/{country}", response_model=list[Place])
def get_places(country: str, manager: PlaceManagerDep):
    return manager.get_itinerary(country)


@router.post("/", response_model=Place)
def create_place(place: Place, manager: PlaceManagerDep):
    return manager.add_place(place)


@router.delete("/{place_id}")
def delete_place(place_id: int, manager: PlaceManagerDep):
    return manager.remove_place(place_id)
