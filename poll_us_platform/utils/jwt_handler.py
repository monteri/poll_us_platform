import time

import jwt

from poll_us_platform.settings import settings

JWT_ALGORITHM = "HS256"
TOKEN_DURATION = 6000


def sign_jwt(user_id: int):
    """Creates token"""
    payload = {
        "user_id": user_id,
        "expiry": time.time() + TOKEN_DURATION,
    }
    return jwt.encode(payload, settings.secret, algorithm=JWT_ALGORITHM)


def decode_jwt(token: str):
    """Decodes token"""
    try:
        decode_token = jwt.decode(token, settings.secret, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token["expiry"] >= time.time() else {}
    except:
        return {}
