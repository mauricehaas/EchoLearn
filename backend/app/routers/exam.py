from typing import Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.exam_simulator import ExamSimulator
from app.services.prompts import (
    clarify,
    evaluate_exam,
    evaluate_student_answer,
    next_question,
    rephrase_question,
)

router = APIRouter(prefix="/exam", tags=["exam"])

exam_simulator = ExamSimulator(
    rephrase_question=rephrase_question,
    evaluate_student_answer=evaluate_student_answer,
    evaluate_exam=evaluate_exam,
    next_question=next_question,
    clarify=clarify,
)


class RephraseQuestionBody(BaseModel):
    """Body for rephrasing a question.

    Args:
        question (str): The question to be rephrased.
    """

    question: str


@router.post("/rephrase_question")
def rephrase_question(body: RephraseQuestionBody) -> Dict[str, str]:
    """Rephrases a question for the student.

    Args:
      unique_exam_id (str): The unique identifier for the exam.
      question (str): The question to be rephrased.

    Returns:
      Dict[str, str]: The rephrased question.
    """
    try:
        response = exam_simulator.rephrase_question(body.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


class AnswerEvaluationBody(BaseModel):
    """Body for evaluating a student's answer.

    Args:
        unique_exam_id (str): The unique identifier for the exam.
        question (str): The question answered by the student.
        student_answer (str): The answer provided by the student.
        correct_answer (str): The correct answer for comparison.
        max_points (int): The max points.
        evaluate_only (bool): If set, there will be no follow up question.
    """

    unique_exam_id: str
    question: str
    student_answer: str
    correct_answer: str
    max_points: int
    evaluate_only: bool
    parent_id: int
    question_type: str


class AnswerEvaluationResponse(BaseModel):
    """Body for evaluating the response

    Args:
        feedback (str): The feedback given by the LLM
        rating (float): The points given by the LLM
        next_action (str): The action to be taken next
        followup_text (str): The text to be returned and spoken in the Frontend
        answer_id (int): The ID of the answer
        next_max_points (int): How many points there are next
        next_answer(str): The answer to come next
    """

    feedback: str
    rating: float
    next_action: str
    followup_text: str
    answer_id: int
    next_max_points: int = 0
    next_answer: str = ""


@router.post(
    "/evaluate_answer",
    response_model=AnswerEvaluationResponse,
)
async def evaluate_answer(
    body: AnswerEvaluationBody,
) -> AnswerEvaluationResponse:
    """Evaluates the student's answer and provides feedback.
    Args:
      question (str): The question answered by the student.
      student_answer (str): The answer provided by the student.
      correct_answer (str): The correct answer for comparison.

    Returns:
      Dict[str, str]: The evaluation of the student's answer."""
    try:
        response = await exam_simulator.evaluate_student_answer(
            unique_exam_id=body.unique_exam_id,
            question=body.question,
            student_answer=body.student_answer,
            correct_answer=body.correct_answer,
            max_points=body.max_points,
            evaluate_only=body.evaluate_only,
            parent_id=body.parent_id,
            question_type=body.question_type,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


class EvaluateExamBody(BaseModel):
    """Body for evaluating the entire exam.

    Args:
        unique_exam_id (str): The unique identifier for the exam to be evaluated.
    """

    unique_exam_id: str


@router.post("/evaluate_exam")
async def evaluate_student_exam(body: EvaluateExamBody) -> Dict[str, str]:
    """Evaluates the entire exam based on stored feedback and ratings.

    Args:
      unique_exam_id (str): The unique identifier for the exam to be evaluated.

    Returns:
      Dict[str, str]: The final evaluation of the exam."""
    try:
        response = await exam_simulator.evaluate_the_exam(body.unique_exam_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
