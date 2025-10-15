"""Router for Countries."""

from fastapi.routing import APIRouter

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("/")
async def get_countries() -> str:
    """GET /countries/."""
    return "Countries !"
