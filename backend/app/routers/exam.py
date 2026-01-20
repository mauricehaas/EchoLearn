from typing import Dict, Union

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.exam_simulator import ExamSimulator
from app.services.prompts import (
    evaluate_exam,
    evaluate_student_answer,
    prompt_case_one_answer_correct_next_specific_question,
    prompt_case_three_student_does_not_understand_question,
    prompt_case_two_answer_partially_correct_question_to_examine_knowledge_gaps,
)

router = APIRouter(prefix="/exam", tags=["exam"])

exam_simulator = ExamSimulator(
    evaluate_student_answer=evaluate_student_answer,
    prompt_case_one=prompt_case_one_answer_correct_next_specific_question,
    prompt_case_two=prompt_case_two_answer_partially_correct_question_to_examine_knowledge_gaps,
    prompt_case_three=prompt_case_three_student_does_not_understand_question,
    evaluate_exam=evaluate_exam,
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
    """

    unique_exam_id: str
    question: str
    student_answer: str
    correct_answer: str


@router.post("/evaluate_answer")
async def evaluate_answer(body: AnswerEvaluationBody) -> Dict[str, str]:
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
