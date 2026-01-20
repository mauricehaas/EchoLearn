from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select

from app.core.db import get_session
from app.models.exam_evaluation_single_answer import ExamEvaluationSingleAnswer

router = APIRouter(
    prefix="/exam_evaluation_single_answers", tags=["exam_evaluation_single_answers"]
)


# Alle Datensätze abrufen
@router.get("/")
async def get_all_exam_evaluation_single_answers():
    async for session in get_session():
        result = await session.execute(select(ExamEvaluationSingleAnswer))
        rows = result.scalars().all()
        return rows


@router.get("/exam/{exam_id}")
async def get_exam_results(exam_id: str):
    async for session in get_session():
        result = await session.execute(
            select(ExamEvaluationSingleAnswer).where(
                ExamEvaluationSingleAnswer.unique_exam_id == exam_id
            )
        )
        rows = result.scalars().all()

        if not rows:
            raise HTTPException(
                status_code=404, detail="No results found for this exam_id"
            )

        return rows
