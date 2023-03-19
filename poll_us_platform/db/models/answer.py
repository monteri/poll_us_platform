from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from poll_us_platform.db.base import Base
from poll_us_platform.db.models.question import Question


class Answer(Base):
    """Answer model"""

    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    content = Column(String(500), nullable=False)

    question = relationship(Question, back_populates="answers")

    def __repr__(self):
        return f"<Answer {self.content}>"
