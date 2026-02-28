from typing import Dict

from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select

from app.core.db import get_session
from app.models.exam_evaluation_single_answer import ExamEvaluationSingleAnswer

router = APIRouter(
    prefix="/exam_evaluation_single_answers", tags=["exam_evaluation_single_answers"]
)


# Alle Datensätze abrufen
# TODO: Add return type
@router.get("/")
async def get_all_exam_evaluation_single_answers():
    """Defines the GET Endpoint for retreiving the Evaluations given to all single answers that were given in an exam

    Returns:
        _type_: _description_
    """
    async for session in get_session():
        result = await session.execute(select(ExamEvaluationSingleAnswer))
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


@router.get("/exam_scores/{exam_id}")
async def get_exam_scores(exam_id: str) -> Dict[str, float | str]:
    """Defines the GET Endpoint for getting the exam scores based on an exam_id

    Args:
        exam_id (str): the ID of the exam

    Raises:
        HTTPException: Raises Exception if no data available for given exam_id

    Returns:
        Dict[str, float | str]: The scores of the exam in structured form
    """
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

        filtered_rows = []
        clarify_map = {}

        for row in rows:
            if row.question_type == "CLARIFY":
                clarify_map[row.parent_id] = row

        for row in rows:
            if row.id in clarify_map:
                continue

            if row.question_type == "CLARIFY":
                filtered_rows.append(row)
                continue

            if row.question_type != "CLARIFY":
                filtered_rows.append(row)

        total_points = sum(float(row.rating) for row in filtered_rows)
        max_points = sum(float(row.max_points) for row in filtered_rows)

        percentage = (total_points / max_points) * 100 if max_points else 0
        grade = calculate_grade(percentage)

        return {
            "total_points": round(total_points, 2),
            "max_points": round(max_points, 2),
            "percentage": round(percentage, 2),
            "grade": grade,
        }


def calculate_grade(percentage: float) -> str:
    """Calculates the final grade based on German skala

    Args:
        perecentage (float): The percentage of correct answers in the exam

    Returns:
        str: The calculated grade
    """

    percentage = round(float(percentage), 2)

    grade_scale = [
        (95, "1,0"),
        (90, "1,3"),
        (85, "1,7"),
        (80, "2,0"),
        (75, "2,3"),
        (70, "2,7"),
        (65, "3,0"),
        (60, "3,3"),
        (55, "3,7"),
        (50, "4,0"),
        (45, "4,3"),
        (40, "4,7"),
        (0, "5,0"),
    ]

    for threshold, grade in grade_scale:
        if percentage >= threshold:
            return grade
