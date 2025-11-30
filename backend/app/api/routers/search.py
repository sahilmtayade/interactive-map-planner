from fastapi import APIRouter

from app.business.search_mgr import SearchManagerDep

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("")
def search_osm(manager: SearchManagerDep, query: str, country: str = "Singapore"):
    return manager.find_location(query, country)
