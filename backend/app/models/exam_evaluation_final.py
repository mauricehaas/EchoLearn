from sqlalchemy import Column, Integer, Text
from app.core.db import Base


class ExamEvaluationFinal(Base):
    __tablename__ = "exam_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    unique_exam_id = Column(Text, nullable=False)
    overall_feedback = Column(Text, nullable=False)
    overall_rating = Column(Text, nullable=False)
