from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.dependencies import get_db_session
from poll_us_platform.services.user.actions import authenticate_user, create_new_user
from poll_us_platform.services.user.models import Token, UserCreate, UserLogin

router = APIRouter()


@router.post("/signup")
async def sign_up(body: UserCreate, db: AsyncSession = Depends(get_db_session)) -> None:
    """Sign up user"""
    try:
        await create_new_user(body, db)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {err}",
        )


@router.post("/token", response_model=Token)
async def token(body: UserLogin, db: AsyncSession = Depends(get_db_session)) -> Token:
    """Get user token"""
    return await authenticate_user(body.email, body.password, db)
