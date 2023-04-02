import uuid
from typing import List, Union

from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.dals.question_dal import QuestionDal
from poll_us_platform.db.models.user import User
from poll_us_platform.services.answers.models import Answer
from poll_us_platform.services.question.models import (
    QuestionCreate,
    QuestionResult,
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
    question_id: Union[int, str],
    current_user: User,
    session: AsyncSession,
) -> Union[QuestionShow, None]:
    async with session.begin():
        question_dal = QuestionDal(session)
        if isinstance(question_id, int):
            return await question_dal.get_question_by_id(question_id, current_user.id)

        return await question_dal.get_question_by_publish_id(question_id)


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


async def get_question_result(
    publish_id: str,
    session: AsyncSession,
) -> Union[QuestionResult, None]:
    async with session.begin():
        question_dal = QuestionDal(session)
        question = await question_dal.get_question_by_publish_id(publish_id)
        if not question:
            return None
        linked_answers = await question_dal.get_linked_answers(publish_id)
        other_answers = await question_dal.get_other_answers(publish_id)
        result = {"other_answers": [answer[0].content for answer in other_answers]}
        all_count = len(other_answers)
        for answer_id, count in linked_answers:
            result[str(answer_id)] = count
            all_count += count

        result["count"] = all_count
        return result
