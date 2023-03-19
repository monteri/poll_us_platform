from typing import Union

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.dals.user_dal import UserDal
from poll_us_platform.services.user.models import Token, UserCreate
from poll_us_platform.utils.hasher import Hasher
from poll_us_platform.utils.jwt_handler import sign_jwt


async def create_new_user(body: UserCreate, session: AsyncSession) -> int:
    async with session.begin():
        user_dal = UserDal(session)
        user = await user_dal.create_user(
            username=body.username,
            email=body.email,
            password=body.password,
        )
        return user.id


async def _get_user_by_email_for_auth(email: str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDal(session)
        return await user_dal.get_user_by_email(
            email=email,
        )


async def authenticate_user(
    email: str,
    password: str,
    db: AsyncSession,
) -> Union[Token, None]:
    user = await _get_user_by_email_for_auth(email=email, session=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDE,
            detail="Credentials are invalid",
        )
    if not Hasher.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Credentials are invalid",
        )
    return Token(access_token=sign_jwt(user.id))
