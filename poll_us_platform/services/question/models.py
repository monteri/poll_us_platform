from typing import Literal

from pydantic import BaseModel

from poll_us_platform.services.answers.models import Answer


class QuestionCreate(BaseModel):
    title: str
    type: Literal["single", "multiple"]
    another_option: bool
    answers: list[str]


class QuestionShow(BaseModel):
    id: int
    user_id: int
    title: str
    type: Literal["single", "multiple"]
    another_option: bool
    answers: list[Answer]

    class Config:
        orm_mode = True


class QuestionUpdate(BaseModel):
    title: str
    type: Literal["single", "multiple"]
    another_option: bool
    answers: list[str]

    class Config:
        orm_mode = True
