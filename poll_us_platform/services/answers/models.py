from pydantic import BaseModel


class Answer(BaseModel):
    id: int
    content: str
    question_id: int

    class Config:
        orm_mode = True
