import csv
import random
from io import StringIO
from typing import Dict, Optional

from fastapi import APIRouter, HTTPException, Response, UploadFile
from pydantic import BaseModel
from sqlalchemy.future import select

from app.core.db import get_session
from app.models.question import Question

router = APIRouter(prefix="/questions", tags=["questions"])


# IMPORT - CSV Import
@router.post("/import")
async def import_questions(file: UploadFile = None) -> Dict[str, int]:
    """Defines POST Endpoint to import questions from a CSV file.
    The file should have two columns: "question" and "answer".
    The endpoint reads the file, creates Question objects, and saves them
    to the database.

    Args:
        file (UploadFile, optional): The uploaded CSV file containing questions and answers. Defaults to None.

    Raises:
        HTTPException: If no file is provided or if the file is not a CSV, an HTTPException with status code 400 is raised.
        HTTPException: If the CSV file is malformed or if there are issues during database operations, an HTTPException with status code 500 may be raised.

    Returns:
        Dict[str, int]: A dictionary with the key "imported" and the value being the number of questions successfully imported.
    """
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
            points = row.get("max_points")
            if not question_text or not answer_text or not points:
                continue

            new_q = Question(
                question=question_text, answer=answer_text, max_points=points or ""
            )
            session.add(new_q)
            created += 1
        await session.commit()

    return {"imported": created}


# EXPORT - CSV Export
@router.get("/export")
async def export_questions() -> Response:
    """Defines the GET Endpoint for exporting the questions

    Returns:
        Response: Exports the questions in a CSV-File
    """
    async for session in get_session():
        result = await session.execute(select(Question))
        questions = result.scalars().all()

    output = "question,answer,max_points\n"
    for q in questions:
        safe_question = q.question.replace('"', '""')
        safe_answer = q.answer.replace('"', '""')
        safe_points = str(q.max_points or "").replace('"', '""')
        output += f'"{safe_question}","{safe_answer}","{safe_points}"\n'

    return Response(
        content=output,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=questions.csv"},
    )


# Alle Fragen abrufen
@router.get("/")
async def get_questions():
    """Defines the GET Endpoint for retrieving all questions

    Returns:
        A list of all questions in the database
    """
    async for session in get_session():
        result = await session.execute(select(Question))
        questions = result.scalars().all()
        return questions


@router.get("/random")
async def get_random_questions():
    """Defines the GET Endpoint for retrieving random questions

    Returns:
        A list of random questions from the database
    """
    async for session in get_session():
        # Alle Fragen abrufen
        result = await session.execute(select(Question))
        questions = result.scalars().all()

        # Zufällig x auswählen (oder weniger, falls <x)
        num_questions = min(7, len(questions))
        random_questions = random.sample(questions, num_questions)

        return random_questions


# Eine Frage nach ID abrufen
@router.get("/{question_id}")
async def get_question(question_id: int):
    """Defines the GET Endpoint for retrieving a question by its ID

    Args:
        question_id (int): The ID of the question to retrieve

    Raises:
        HTTPException: If no question with the given ID is found, an HTTPException with status
        code 404 is raised.

    Returns:
        The question object with the specified ID
    """
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
    """Defines the schema for creating a new question

    Attributes:
        question (str): The text of the question
        answer (str): The text of the answer
    """

    question: str
    answer: str
    max_points: str


@router.post("/")
async def create_question(data: QuestionCreate):
    """Defines the POST Endpoint for creating a new question

    Args:
        data (QuestionCreate): The data for the new question, including the question text and answer text

    Returns:
        The newly created question object
    """
    async for session in get_session():
        new_question = Question(
            question=data.question, answer=data.answer, max_points=data.max_points
        )

        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)

        return new_question


# DELETE – Frage löschen
@router.delete("/{question_id}")
async def delete_question(question_id: int) -> Dict[str, str]:
    """Defines the DELETE Endpoint for deleting a question by its ID

    Args:
        question_id (int): The ID of the question to delete

    Raises:
        HTTPException: If no question with the given ID is found, an HTTPException with status
        code 404 is raised.

    Returns:
        Dict[str, str]: A dictionary with a message confirming the successful deletion of the question
    """
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
    """Defines the schema for updating an existing question

    Attributes:
        question (Optional[str]): The new text of the question (optional)
        answer (Optional[str]): The new text of the answer (optional)
    """

    question: Optional[str] = None
    answer: Optional[str] = None
    max_points: Optional[str] = None


# PATCH – Frage bearbeiten
@router.patch("/{question_id}")
async def update_question(question_id: int, data: QuestionUpdate):
    """Defines the PATCH Endpoint for updating an existing question by its ID

    Args:
        question_id (int): The ID of the question to update
        data (QuestionUpdate): The data for updating the question, which may include a new question
        text and/or a new answer text. Both fields are optional.

    Raises:
        HTTPException: If no question with the given ID is found, an HTTPException with status
        code 404 is raised.

    Returns:
        The updated question object with the new values
    """
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
        if data.max_points is not None:
            question.max_points = data.max_points

        await session.commit()
        await session.refresh(question)

        return question
