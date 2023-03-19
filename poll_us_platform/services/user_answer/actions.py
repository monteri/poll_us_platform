from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.dals.user_answer_dal import UserAnswerDal
from poll_us_platform.db.models.user import User
from poll_us_platform.services.user_answer.models import UserAnswerCreate


async def create_new_user_answer(
    body: UserAnswerCreate,
    current_user: User,
    session: AsyncSession,
) -> bool:
    async with session.begin():
        user_answer_dal = UserAnswerDal(session)
        await user_answer_dal.create_user_answer(
            user_id=current_user.id,
            question_id=body.question_id,
            answer_id=body.answer_id,
            content=body.content,
        )
        return True
