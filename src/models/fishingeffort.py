"""Model for describing fishing efforts."""

from datetime import datetime

from pydantic import BaseModel


class FishingEffort(BaseModel):
    """FishingEffort."""

    lat: float = 0
    lon: float = 0
    start: datetime
    end: datetime
