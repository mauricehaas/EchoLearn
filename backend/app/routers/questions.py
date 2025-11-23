from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_session
from app.models.question import Question

router = APIRouter(prefix="/questions", tags=["questions"])


# Alle Fragen abrufen
@router.get("/")
async def get_questions(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Question))
    questions = result.scalars().all()
    return questions


# Eine Frage nach ID abrufen
@router.get("/{question_id}")
async def get_question(question_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
