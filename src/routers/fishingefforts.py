"""Router for Fishing Efforts."""

from fastapi.routing import APIRouter

router = APIRouter(prefix="/fishingefforts", tags=["Fishing Efforts"])


@router.get("/")
async def get_fishing_efforts() -> str:
    """GET /fishingefforts/."""
    return "Fishing Efforts !"
