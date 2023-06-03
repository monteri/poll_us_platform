from typing import List, Union

from sqlalchemy import and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.models.answer import Answer
from poll_us_platform.db.models.question import Question
from poll_us_platform.db.models.user_answer import UserAnswer


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
        return [question[0] for question in questions]

    async def get_question_by_id(
        self,
        question_id: int,
        user_id: int = None,
    ) -> Union[Question, None]:
        """Finds question by id"""
        query = select(Question).where(Question.id == question_id)
        if user_id:
            query = query.where(Question.user_id == user_id)
        user = await self.db_session.execute(query)
        user_row = user.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_question_by_publish_id(
        self,
        publish_id: str,
    ) -> Union[Question, None]:
        """Finds question by publish id"""
        query = select(Question).where(Question.publish_id == publish_id)
        question = await self.db_session.execute(query)
        question_row = question.fetchone()
        if question_row is not None:
            return question_row[0]

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

    async def get_linked_answers(
        self,
        publish_id: str,
    ) -> list[tuple[Union[int, None], int]]:
        """Returns grouped answers for specific question"""
        group_query = (
            select(
                UserAnswer.answer_id,
                func.count(UserAnswer.id),
            )
            .filter(
                UserAnswer.publish_id == publish_id,
                UserAnswer.answer_id.isnot(None),
            )
            .group_by(
                UserAnswer.answer_id,
            )
        )
        group_result = await self.db_session.execute(group_query)
        return group_result.fetchall()

    async def get_other_answers(
        self,
        publish_id: str,
    ) -> list[tuple[UserAnswer, None]]:
        """return grouped answers for specific question"""
        other_answers_query = select(UserAnswer).filter(
            UserAnswer.publish_id == publish_id,
            UserAnswer.answer_id.is_(None),
        )
        other_answers_result = await self.db_session.execute(other_answers_query)
        return other_answers_result.fetchall()
