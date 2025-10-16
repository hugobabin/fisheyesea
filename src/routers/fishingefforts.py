"""Router for Fishing Efforts."""

from fastapi.routing import APIRouter

from models.fishingeffort import FishingEffort
from services.db.duck import ServiceDuck

router = APIRouter(prefix="/fishingefforts", tags=["Fishing Efforts"])


@router.get("/")
async def get_fishing_efforts() -> list[FishingEffort]:
    """GET /fishingefforts/."""
    ServiceDuck.connect()
    return ServiceDuck.get_data()
