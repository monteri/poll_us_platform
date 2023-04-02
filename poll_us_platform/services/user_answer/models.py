from fastapi import HTTPException, status
from pydantic import BaseModel, Field, root_validator
from pydantic.fields import Optional


class UserAnswerCreate(BaseModel):
    publish_id: str
    answer_id: Optional[int]
    content: Optional[str] = Field(None, max_length=500)

    @root_validator
    def validate_answer_id_or_content(cls, values):
        if not values.get("answer_id", None) and not values.get("content", None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="answer_id or content should be present",
            )
        return values


class UserAnswerShow(BaseModel):
    id: int
    user_id: int
    publish_id: str
    answer_id: Optional[str]
    content: Optional[str] = Field(None, max_length=500)

    class Config:
        orm_mode = True
