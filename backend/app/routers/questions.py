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


# CREATE – neue Frage anlegen
class QuestionCreate(BaseModel):
    question: str
    answer: str


@router.post("/")
async def create_question(data: QuestionCreate):
    async for session in get_session():
        new_question = Question(
            question=data.question,
            answer=data.answer
        )

        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)

        return new_question


# DELETE – Frage löschen
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


# UPDATE – Schema
class QuestionUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None


# PATCH – Frage bearbeiten
@router.patch("/{question_id}")
async def update_question(question_id: int, data: QuestionUpdate):
    async for session in get_session():

        result = await session.execute(
            select(Question).where(Question.id == question_id)
        )
        question = result.scalar_one_or_none()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        if data.question is not None:
            question.question = data.question
        if data.answer is not None:
            question.answer = data.answer

        await session.commit()
        await session.refresh(question)

        return question
