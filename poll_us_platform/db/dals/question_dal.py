from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.models.answer import Answer
from poll_us_platform.db.models.question import Question


class QuestionDal:
    """Question database access layer"""

    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_question(
        self,
        user_id: int,
        title: str,
        _type: str,
        answers: list[str],
        another_option: bool = False,
    ) -> Question:
        """Creates question"""
        new_answers = [Answer(content=answer) for answer in answers]
        new_question = Question(
            user_id=user_id,
            title=title,
            type=_type,
            another_option=another_option,
            answers=new_answers,
        )
        self.db_session.add(new_question)
        self.db_session.add_all(new_answers)
        await self.db_session.flush()
        return new_question

    async def get_questions_by_user(self, user_id: int) -> List[Question]:
        """Finds question by user_id"""
        query = select(Question).where(Question.user_id == user_id)
        questions = await self.db_session.execute(query)
        return [question for question, _ in questions]

    async def get_question_by_id(
        self,
        question_id: int,
        user_id: int = None,
    ) -> Question:
        """Finds question by id"""
        query = select(Question).where(Question.id == question_id)
        if user_id:
            query = query.where(Question.user_id == user_id)
        user = await self.db_session.execute(query)
        user_row = user.fetchone()
        if user_row is not None:
            return user_row[0]

    async def delete_question(self, question_id: int, user_id: int = None) -> None:
        """Deletes question"""
        query = delete(Question).where(Question.id == question_id)
        if user_id:
            query = query.where(Question.user_id == user_id)
        await self.db_session.execute(query)

    async def update_question(
        self,
        question_id: int,
        title: str,
        _type: str,
        answers: list[str],
        another_option: bool,
        answers_changed: bool,
        user_id: int = None,
    ) -> None:
        """Updates question"""
        if answers_changed:
            delete_query = delete(Answer).where(Answer.question_id == question_id)
            new_answers = [
                Answer(question_id=question_id, content=answer) for answer in answers
            ]
            await self.db_session.execute(delete_query)
            self.db_session.add_all(new_answers)

        query = (
            update(Question)
            .values(
                {
                    "title": title,
                    "type": _type,
                    "another_option": another_option,
                },
            )
            .where(Question.id == question_id)
        )
        if user_id:
            query = query.where(Question.user_id == user_id)

        await self.db_session.execute(query)

    async def update_publish_id(
        self,
        question_id: int,
        publish_id: str,
        user_id: int = None,
    ) -> None:
        """Updates publish_id"""
        query = (
            update(Question)
            .values(
                {
                    "publish_id": publish_id,
                },
            )
            .where(Question.id == question_id)
        )
        if user_id:
            query = query.where(Question.user_id == user_id)
        await self.db_session.execute(query)
