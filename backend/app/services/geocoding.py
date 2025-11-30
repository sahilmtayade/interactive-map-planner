from typing import Annotated

from fastapi import Depends
from geopy.geocoders import Nominatim

from app.models.config import AppConfig, ConfigDep


class GeocodingService:
    def __init__(self, config: AppConfig):
        self.client = Nominatim(user_agent=config.GEO_USER_AGENT)


# --- PROVIDER ---
def get_geo_service(config: ConfigDep) -> GeocodingService:
    return GeocodingService(config)


# --- DEPENDENCY ALIAS ---
GeoServiceDep = Annotated[GeocodingService, Depends(get_geo_service)]
