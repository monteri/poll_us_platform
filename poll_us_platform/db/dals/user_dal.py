from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from poll_us_platform.db.models.user import User
from poll_us_platform.utils.hasher import Hasher


class UserDal:
    """User database access layer"""

    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_user(self, username: str, email: str, password: str) -> User:
        """Creates user"""
        hashed_password = Hasher.get_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        """Finds user by email"""
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_id(self, user_id: str) -> Union[User, None]:
        """Finds user by id"""
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
