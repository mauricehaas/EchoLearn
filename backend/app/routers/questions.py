import csv
import random
from io import StringIO
from typing import Optional

from fastapi import APIRouter, HTTPException, Response, UploadFile
from pydantic import BaseModel
from sqlalchemy.future import select

from app.core.db import get_session
from app.models.question import Question

router = APIRouter(prefix="/questions", tags=["questions"])


# IMPORT - CSV Import
@router.post("/import")
async def import_questions(file: UploadFile = None):
    if file is None:
        raise HTTPException(status_code=400, detail="No file provided")
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    content = await file.read()
    csv_text = content.decode("utf-8")
    reader = csv.DictReader(StringIO(csv_text))

    created = 0
    async for session in get_session():
        for row in reader:
            question_text = row.get("question")
            answer_text = row.get("answer")
            if not question_text:
                continue

            new_q = Question(question=question_text, answer=answer_text or "")
            session.add(new_q)
            created += 1
        await session.commit()

    return {"imported": created}


# EXPORT - CSV Export
@router.get("/export")
async def export_questions():
    async for session in get_session():
        result = await session.execute(select(Question))
        questions = result.scalars().all()

    output = "question,answer\n"
    for q in questions:
        safe_question = q.question.replace('"', '""')
        safe_answer = q.answer.replace('"', '""')
        output += f'"{safe_question}","{safe_answer}"\n'

    return Response(
        content=output,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=questions.csv"},
    )


# Alle Fragen abrufen
@router.get("/")
async def get_questions():
    async for session in get_session():
        result = await session.execute(select(Question))
        questions = result.scalars().all()
        return questions
    
@router.get("/random")
async def get_random_questions():
    async for session in get_session():
        # Alle Fragen abrufen
        result = await session.execute(select(Question))
        questions = result.scalars().all()
        
        # Zufällig x auswählen (oder weniger, falls <x)
        num_questions = min(3, len(questions))
        random_questions = random.sample(questions, num_questions)
        
        return random_questions


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
        new_question = Question(question=data.question, answer=data.answer)

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
