from sqlalchemy.orm import DeclarativeBase

from poll_us_platform.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
