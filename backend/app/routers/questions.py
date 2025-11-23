from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.future import select

from app.core.db import get_session
from app.models.question import Question

router = APIRouter(prefix="/questions", tags=["questions"])


# Alle Fragen abrufen
@router.get("/")
async def get_questions():
    async for session in get_session():
        result = await session.execute(select(Question))
        questions = result.scalars().all()
        return questions


# Eine Frage nach ID abrufen
@router.get("/{question_id}")
async def get_question(question_id: int):
    async for session in get_session():
        result = await session.execute(
            select(Question).where(Question.id == question_id)
        )
        question = result.scalar_one_or_none()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        return question


# Frage löschen
@router.delete("/{question_id}")
async def delete_question(question_id: int):
    async for session in get_session():
        result = await session.execute(
            select(Question).where(Question.id == question_id)
        )
        question = result.scalar_one_or_none()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        await session.delete(question)
        await session.commit()

        return {"message": "Question deleted successfully"}


# Update-Schema
class QuestionUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None


# Frage bearbeiten
@router.patch("/{question_id}")
async def update_question(question_id: int, data: QuestionUpdate):
    async for session in get_session():

        # Frage holen
        result = await session.execute(
            select(Question).where(Question.id == question_id)
        )
        question = result.scalar_one_or_none()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Nur geänderte Felder übernehmen
        if data.question is not None:
            question.question = data.question
        if data.answer is not None:
            question.answer = data.answer

        await session.commit()
        await session.refresh(question)

        return question
