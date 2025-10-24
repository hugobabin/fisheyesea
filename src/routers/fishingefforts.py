"""Router for Fishing Efforts."""

from fastapi import Depends
from fastapi.routing import APIRouter

from models.fishingeffort import FishingEffort
from services.db.duck import ServiceDuck
from services.jwt import get_current_user

router = APIRouter(prefix="/fishingefforts", tags=["Fishing Efforts"])


@router.get("/")
async def get_fishing_efforts(
    user: dict = Depends(get_current_user),
) -> list[FishingEffort]:
    """GET /fishingefforts/."""
    ServiceDuck.connect()
    return ServiceDuck.get_data()
