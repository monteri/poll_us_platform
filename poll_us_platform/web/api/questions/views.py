from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.dependencies import get_db_session
from poll_us_platform.db.models.user import User
from poll_us_platform.services.question.actions import (
    create_new_question,
    delete_question,
    get_question_result,
    get_single_question,
    get_user_questions,
    publish_question,
    update_question,
)
from poll_us_platform.services.question.models import (
    QuestionCreate,
    QuestionResult,
    QuestionShow,
    QuestionUpdate,
)
from poll_us_platform.utils.current_user import get_current_user

router = APIRouter()


@router.post("/questions/{pk}/publish")
async def question_publish(
    pk: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> str:
    """Publish question"""
    return await publish_question(pk, current_user, db)


@router.get("/questions/{publish_id}/result")
async def question_result(
    publish_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> QuestionResult:
    """Get question result"""
    return await get_question_result(publish_id, db)


@router.post("/questions")
async def question_create(
    body: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> QuestionShow:
    """Create question"""
    return await create_new_question(body, current_user, db)


@router.get("/questions")
async def questions_list(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[QuestionShow]:
    """Get questions list"""
    return await get_user_questions(current_user, db)


@router.get("/questions/{pk}")
async def question_show(
    pk: Union[int, str],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> Union[QuestionShow, None]:
    """Show single question"""
    return await get_single_question(pk, current_user, db)


@router.delete("/questions/{pk}")
async def question_delete(
    pk: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> bool:
    """Delete question"""
    return await delete_question(pk, current_user, db)


@router.put("/questions/{pk}")
async def question_update(
    pk: int,
    body: QuestionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> bool:
    """Update questions"""
    return await update_question(pk, body, current_user, db)
