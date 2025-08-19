from sqlmodel import SQLModel, create_engine, Session, Field

class FishingEffort(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: str
    lat_lon: str
    hours: int