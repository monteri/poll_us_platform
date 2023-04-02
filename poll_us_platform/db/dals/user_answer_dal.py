from typing import Union

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.models.user_answer import UserAnswer


class UserAnswerDal:
    """UserAnswer database access layer"""

    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_user_answer(
        self,
        user_id: int,
        publish_id: str,
        content: str = None,
        answer_id: int = None,
    ) -> UserAnswer:
        """Creates UserAnswer"""
        new_user_answer = UserAnswer(
            user_id=user_id,
            publish_id=publish_id,
            content=content,
            answer_id=answer_id,
        )
        self.db_session.add(new_user_answer)
        await self.db_session.flush()
        return new_user_answer

    async def get_user_answer_by_question_and_user(
        self,
        publish_id: str,
        user_id: int,
    ) -> Union[UserAnswer, None]:
        """Finds question by publish id"""
        query = select(UserAnswer).where(
            UserAnswer.publish_id == publish_id,
            UserAnswer.user_id == user_id,
        )
        question = await self.db_session.execute(query)
        question_row = question.fetchone()
        if question_row is not None:
            return question_row[0]
