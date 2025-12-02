from sqlalchemy import Column, Integer, Text
from app.core.db import Base


class ExamEvaluationSingleAnswer(Base):
    __tablename__ = "exam_simulations"

    id = Column(Integer, primary_key=True, index=True)
    unique_exam_id = Column(Text, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    feedback = Column(Text, nullable=False)
    rating = Column(Text, nullable=False)
