from sqlalchemy import Column, Integer, Text

from app.core.db import Base


class ExamEvaluationFinal(Base):
    """Database Schema for the Table ExamEvaluationFinal

    Args:
        id (int): The primary key of the evaluation
        unique_exam_id (str): The unique exam identifier
        overall_feedback (str): The feedback to the exam
    """

    __tablename__ = "exam_evaluation_final"

    id = Column(Integer, primary_key=True, index=True)
    unique_exam_id = Column(Text, nullable=False)
    overall_feedback = Column(Text, nullable=False)
