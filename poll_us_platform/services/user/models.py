from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, validator

MIN_NAME_LENGTH = 3
MIN_PASSWORD_LENGTH = 6


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator("username")
    def validate_name(cls, value):
        if len(value) < MIN_NAME_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username should contain more than 3 symbols",
            )
        return value

    @validator("password")
    def validate_surname(cls, value):
        if len(value) < MIN_PASSWORD_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTIT,
                detail="Password should contain more than 6 symbols",
            )
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
