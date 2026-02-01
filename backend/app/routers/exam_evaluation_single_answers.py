from typing import Dict

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


@router.get("/exam_scores/{exam_id}")
async def get_exam_scores(exam_id: str) -> Dict[str, float | str]:
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
    """
    Berechnet die Note nach gängiger deutscher Prozent-Noten-Umrechnung
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
