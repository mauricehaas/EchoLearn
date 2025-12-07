from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from difflib import SequenceMatcher
from sqlalchemy.future import select
from app.core.db import get_session
from app.models.question import Question

router = APIRouter(prefix="/learn", tags=["learn"])


class AnswerCheck(BaseModel):
    question_id: int
    answer: str


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


@router.post("/check")
async def check_answer(data: AnswerCheck):
    async for session in get_session():
        result = await session.execute(
            select(Question).where(Question.id == data.question_id)
        )
        question_entry = result.scalar_one_or_none()
        if not question_entry:
            raise HTTPException(status_code=404, detail="Question not found")

        expected = question_entry.answer
        user_answer = data.answer

        score = similarity(user_answer, expected)

        if score > 0.8:
            feedback = "Richtig!"
        elif score > 0.5:
            feedback = "Fast richtig, überprüfe nochmal."
        else:
            feedback = "Falsch, probiere es erneut."

        return {"feedback": feedback, "score": score}
