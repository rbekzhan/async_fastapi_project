import httpx
from fastapi import HTTPException, status
from app.core.config import settings
from app.models.schemas import CatFactResponse

async def fetch_cat_fact() -> CatFactResponse:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.cat_api_url, timeout=5.0)
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error while requesting cat fact: {exc}"
        )
    try:
        response.raise_for_status()
        return CatFactResponse(**response.json())
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"API returned error: {exc.response.text}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error parsing cat fact: {exc}"
        )
