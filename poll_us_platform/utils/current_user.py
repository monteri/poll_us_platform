from typing import Union

from fastapi import HTTPException, Request, status

from poll_us_platform.db.dals.user_dal import UserDal
from poll_us_platform.db.models.user import User
from poll_us_platform.utils.jwt_handler import decode_jwt


async def get_current_user(
    request: Request,
) -> Union[User, None]:
    """Returns current user from token"""
    session = request.app.state.db_session_factory
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = decode_jwt(token)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except:
        raise credentials_exception

    async with session.begin():
        user = await UserDal(session).get_user_by_id(id=user_id)
        if user is None:
            raise credentials_exception
        return user
