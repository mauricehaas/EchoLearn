from typing import Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.exam_simulator import ExamSimulator
from app.models.prompts import begin_exam, evaluate_student_answer, evaluate_exam

router = APIRouter(prefix="/exam", tags=["exam"])

exam_simulator = ExamSimulator(
    begin_exam=begin_exam,
    evaluate_student_answer=evaluate_student_answer,
    evaluate_exam=evaluate_exam,
)


@router.post("/begin_exam")
async def start_exam() -> Dict[str, str]:
    """Starts the exam simulation and returns the first question.

    Returns:
      Dict[str, str]: The first question of the exam.
    """
    try:
        response = exam_simulator.begin_exam()
        return {"first_question": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AnswerEvaluationBody(BaseModel):
    student_answer: str
    correct_answer: str


@router.post("/evaluate_answer")
async def evaluate_answer(body: AnswerEvaluationBody) -> Dict[str, str]:
    """Evaluates the student's answer and provides feedback.
    Args:
      student_answer (str): The answer provided by the student.
      correct_answer (str): The correct answer for comparison.

    Returns:
      Dict[str, str]: The evaluation of the student's answer."""
    try:
        response = exam_simulator.evaluate_student_answer(
            body.student_answer, body.correct_answer
        )
        return {"answer_evaluation": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class EvaluateExamBody(BaseModel):
    unique_exam_id: str


@router.post("/evaluate_exam")
async def evaluate_student_exam(body: EvaluateExamBody) -> Dict[str, str]:
    """Evaluates the entire exam based on stored feedback and ratings.

    Args:
      unique_exam_id (str): The unique identifier for the exam to be evaluated.

    Returns:
      Dict[str, str]: The final evaluation of the exam."""
    try:
        response = exam_simulator.evaluate_the_exam(body.unique_exam_id)
        return {"final_exam_evaluation": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
