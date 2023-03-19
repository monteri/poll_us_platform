from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """Hasher class"""

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Verifies user's password"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Creates password hash"""
        return pwd_context.hash(password)
