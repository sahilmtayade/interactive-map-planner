from typing import Annotated

from fastapi import Depends
from geopy.location import Location as GeoLocation

from app.services.geocoding import GeocodingService, GeoServiceDep


class OsmRepository:
    def __init__(self, geo_service: GeocodingService):
        self.client = geo_service.client

    def search(self, query: str, context: str) -> GeoLocation | None:
        try:
            # Contextual search
            loc = self.client.geocode(f"{query}, {context}", timeout=5)
            if loc:
                return loc
            # Global fallback
            return self.client.geocode(query, timeout=5)
        except Exception:
            return None


# --- PROVIDER ---
def get_osm_repo(geo_service: GeoServiceDep) -> OsmRepository:
    return OsmRepository(geo_service)


# --- DEPENDENCY ALIAS ---
OsmRepoDep = Annotated[OsmRepository, Depends(get_osm_repo)]
