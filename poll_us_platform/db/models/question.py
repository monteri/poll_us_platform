from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from poll_us_platform.db.base import Base
from poll_us_platform.db.models.user import User

QUESTION_TYPES = ["single", "multiple"]


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String(255), nullable=False)
    type = Column(String(64), nullable=False)
    another_option = Column(Boolean, default=False)
    publish_id = Column(String(64), nullable=True, unique=True)

    user = relationship(User, remote_side="User.id")
    answers = relationship(
        "Answer",
        back_populates="question",
        passive_deletes=True,
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Question {self.title}>"
