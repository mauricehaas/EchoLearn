from sqlalchemy import Column, Integer, Text

from app.core.db import Base


class ExamEvaluationSingleAnswer(Base):
    """Database schema for the table ExamEvaluationSingleAnswer

    Attributes:
        id (int): The primary key for the table
        parent_id (int): The id of the previous question, 0 if no parent question attached, ≠0 if question of type "CLARIFY"
        unique_exam_id (str): Unique exam identifier
        question_type (str): Determine whether "BASE" or "CLARIFY" question
        question (str): The text of a question in German
        student_answer (str): The answer provided by the user to a question in German
        correct_answer (str): The correct answer annotated for the question in German
        feedback (str): Feedback provided by the LLM on the given student answer in German
        rating (str): The points received for the given student answer
        max_points (str): The maximal points that can be received for this question
    """

    __tablename__ = "exam_evaluation_single_answer"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer)
    unique_exam_id = Column(Text, nullable=False)
    question_type = Column(Text, nullable=False)
    question = Column(Text, nullable=False)
    student_answer = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    feedback = Column(Text, nullable=False)
    rating = Column(Text, nullable=False)
    max_points = Column(Text, nullable=False)
