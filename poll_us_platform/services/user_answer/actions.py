from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.dals.user_answer_dal import UserAnswerDal
from poll_us_platform.db.models.user import User
from poll_us_platform.services.user_answer.models import (
    UserAnswerCreate,
    UserAnswerShow,
)


async def create_new_user_answer(
    body: UserAnswerCreate,
    current_user: User,
    session: AsyncSession,
) -> bool:
    async with session.begin():
        user_answer_dal = UserAnswerDal(session)
        await user_answer_dal.create_user_answer(
            user_id=current_user.id,
            publish_id=body.publish_id,
            answer_id=body.answer_id,
            content=body.content,
        )
        return True


async def get_single_user_answer(
    publish_id: str,
    current_user: User,
    session: AsyncSession,
) -> Union[UserAnswerShow, None]:
    async with session.begin():
        user_answer_dal = UserAnswerDal(session)
        return await user_answer_dal.get_user_answer_by_question_and_user(
            publish_id,
            current_user.id,
        )
