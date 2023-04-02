from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.dependencies import get_db_session
from poll_us_platform.db.models.user import User
from poll_us_platform.services.user_answer.actions import (
    create_new_user_answer,
    get_single_user_answer,
)
from poll_us_platform.services.user_answer.models import (
    UserAnswerCreate,
    UserAnswerShow,
)
from poll_us_platform.utils.current_user import get_current_user

router = APIRouter()


@router.post("/user_answers")
async def user_answer_create(
    body: UserAnswerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> bool:
    """Create User Answer"""
    try:
        return await create_new_user_answer(body, current_user, db)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {err}",
        )


@router.get("/user_answers/{publish_id}")
async def user_answer_show(
    publish_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> Union[UserAnswerShow, None]:
    """Show single user answer"""
    return await get_single_user_answer(publish_id, current_user, db)
