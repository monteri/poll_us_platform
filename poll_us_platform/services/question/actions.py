import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.dals.question_dal import QuestionDal
from poll_us_platform.db.models.user import User
from poll_us_platform.services.answers.models import Answer
from poll_us_platform.services.question.models import (
    QuestionCreate,
    QuestionShow,
    QuestionUpdate,
)


async def create_new_question(
    body: QuestionCreate,
    current_user: User,
    session: AsyncSession,
) -> QuestionShow:
    async with session.begin():
        question_dal = QuestionDal(session)
        question = await question_dal.create_question(
            user_id=current_user.id,
            title=body.title,
            _type=body.type,
            another_option=body.another_option,
            answers=body.answers,
        )
        return QuestionShow(
            id=question.id,
            user_id=question.user_id,
            title=question.title,
            type=question.type,
            another_option=question.another_option,
            answers=[
                Answer(
                    id=answer.id,
                    content=answer.content,
                    question_id=answer.question_id,
                )
                for answer in question.answers
            ],
        )


async def get_user_questions(
    current_user: User,
    session: AsyncSession,
) -> List[QuestionShow]:
    async with session.begin():
        question_dal = QuestionDal(session)
        return await question_dal.get_questions_by_user(current_user.id)


async def get_single_question(
    question_id: int,
    current_user: User,
    session: AsyncSession,
) -> QuestionShow:
    async with session.begin():
        question_dal = QuestionDal(session)
        return await question_dal.get_question_by_id(question_id, current_user.id)


async def delete_question(
    question_id: int,
    current_user: User,
    session: AsyncSession,
) -> bool:
    async with session.begin():
        question_dal = QuestionDal(session)
        await question_dal.delete_question(question_id, current_user.id)
        return True


def _answers_have_changes(old_answers, new_answers):
    if len(old_answers) != len(new_answers):
        return True

    for idx, old_answer in enumerate(old_answers):
        if old_answer.content != new_answers[idx]:
            return True
    return False


async def update_question(
    question_id: int,
    body: QuestionUpdate,
    current_user: User,
    session: AsyncSession,
) -> bool:
    async with session.begin():
        question_dal = QuestionDal(session)
        question = await question_dal.get_question_by_id(question_id)
        answers_changed = _answers_have_changes(question.answers, body.answers)

        await question_dal.update_question(
            question_id=question_id,
            user_id=current_user.id,
            title=body.title,
            _type=body.type,
            another_option=body.another_option,
            answers=body.answers,
            answers_changed=answers_changed,
        )
        return True


async def publish_question(
    question_id: int,
    current_user: User,
    session: AsyncSession,
) -> str:
    async with session.begin():
        question_dal = QuestionDal(session)
        publish_id = str(uuid.uuid4())
        await question_dal.update_publish_id(
            question_id,
            publish_id,
            current_user.id,
        )
        return publish_id
