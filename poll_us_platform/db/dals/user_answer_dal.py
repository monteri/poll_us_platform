from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.models.user_answer import UserAnswer


class UserAnswerDal:
    """UserAnswer database access layer"""

    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_user_answer(
        self,
        user_id: int,
        question_id: int,
        content: str = None,
        answer_id: int = None,
    ) -> UserAnswer:
        """Creates UserAnswer"""
        new_user_answer = UserAnswer(
            user_id=user_id,
            question_id=question_id,
            content=content,
            answer_id=answer_id,
        )
        self.db_session.add(new_user_answer)
        await self.db_session.flush()
        return new_user_answer
