from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.dependencies import get_db_session
from poll_us_platform.db.models.user import User
from poll_us_platform.services.user.actions import (
    authenticate_user,
    create_new_user,
    retrieve_current_user,
)
from poll_us_platform.services.user.models import Token, UserCreate, UserLogin, UserShow
from poll_us_platform.utils.current_user import get_current_user

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


@router.get("/current_user", response_model=UserShow)
async def current_user_show(
    current_user: User = Depends(get_current_user),
) -> Union[UserShow, None]:
    """Get current user"""
    return retrieve_current_user(current_user)
