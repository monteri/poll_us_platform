from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from poll_us_platform.db.base import Base
from poll_us_platform.db.models.answer import Answer
from poll_us_platform.db.models.question import Question
from poll_us_platform.db.models.user import User


class UserAnswer(Base):
    """UserAnswer model"""

    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    publish_id = Column(String(64), ForeignKey("questions.publish_id"), nullable=False)
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=True)
    content = Column(String(500), nullable=True)

    user = relationship(User, remote_side="User.id")
    question = relationship(Question, remote_side="Question.publish_id")
    answer = relationship(Answer, remote_side="Answer.id")

    def __repr__(self):
        return f"<UserAnswer {self.content}>"
