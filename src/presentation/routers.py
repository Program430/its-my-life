from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.core.database.engine import engine

main_router = APIRouter(prefix="", tags=["main_routers"])


@main_router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@main_router.get("/health/db")
async def check_database():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        return {"database": "ok"}

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )
