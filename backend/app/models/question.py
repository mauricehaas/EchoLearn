from sqlalchemy import Column, Integer, Text

from app.core.db import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    max_points = Column(Text, nullable=False)
