from typing import Annotated, Any

from fastapi import Depends, HTTPException

from app.dataaccess.osm_repo import OsmRepoDep, OsmRepository


class SearchManager:
    def __init__(self, repo: OsmRepository):
        self.repo = repo

    def find_location(self, query: str, country: str) -> dict[str, Any]:
        loc = self.repo.search(query, country)
        if not loc:
            raise HTTPException(status_code=404, detail="Location not found")

        return {
            "name": query,
            "address": loc.address,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "found": True,
        }


# --- PROVIDER ---
def get_search_mgr(repo: OsmRepoDep) -> SearchManager:
    return SearchManager(repo)


# --- DEPENDENCY ALIAS ---
SearchManagerDep = Annotated[SearchManager, Depends(get_search_mgr)]
