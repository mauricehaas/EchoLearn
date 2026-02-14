from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select

from app.core.db import get_session
from app.models.exam_evaluation_final import ExamEvaluationFinal

router = APIRouter(prefix="/exam_evaluation_final", tags=["exam_evaluation_final"])


# Alle Datensätze abrufen
# TODO: Add return type
@router.get("/")
async def get_all_exam_evaluation_final():
    """Defines the GET Endpoint for retreiving the final exam evaluation

    Returns:
        _type_: _description_
    """
    async for session in get_session():
        result = await session.execute(select(ExamEvaluationFinal))
        rows = result.scalars().all()
        return rows


# TODO: Add return type
@router.get("/exam/{exam_id}")
async def get_exam_results(exam_id: str):
    """Defines the GET Endpoint for retreiving the exam results based on an exam_id

    Args:
        exam_id (str): ID for retreiving exam results

    Raises:
        HTTPException: Throws an Exception if no exam results for a specific exam_id are found

    Returns:
        _type_: _description_
    """
    async for session in get_session():
        result = await session.execute(
            select(ExamEvaluationFinal).where(
                ExamEvaluationFinal.unique_exam_id == exam_id
            )
        )
        rows = result.scalars().all()

        if not rows:
            raise HTTPException(
                status_code=404, detail="No results found for this exam_id"
            )

        return rows
