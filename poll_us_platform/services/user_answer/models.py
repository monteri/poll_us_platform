from fastapi import HTTPException, status
from pydantic import BaseModel, Field, root_validator
from pydantic.fields import Optional


class UserAnswerCreate(BaseModel):
    question_id: int
    answer_id: Optional[int]
    content: Optional[str] = Field(None, max_length=500)

    @root_validator
    def validate_answer_id_or_content(self, values):
        if not values.get("answer_id", None) and not values.get("content", None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="answer_id or content should be present",
            )
        return values
