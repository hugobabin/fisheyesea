"""Router for Security."""

from fastapi.routing import APIRouter

from services.jwt import create_access_token

router = APIRouter(prefix="/security", tags=["Security"])


@router.get("/token")
async def get_token() -> str:
    """GET a new access token."""
    return create_access_token({"sub": "fisheyesea-api-access"})
