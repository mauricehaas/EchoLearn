from sqlalchemy import Column, Integer, Text

from app.core.db import Base


class Question(Base):
    """Database Schema for Table Question

    Args:
        id (int): unique question identifier, primary key
        question (str): question text in German
        answer (str): correct answer to the question in German
        max_points (str): maximal achievable points for the question
    """

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    max_points = Column(Text, nullable=False)
