from sqlmodel import Field, SQLModel


class Place(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    category: str
    address: str
    latitude: float
    longitude: float
    notes: str | None = None
    country: str = "Singapore"
    zone: str | None = None
