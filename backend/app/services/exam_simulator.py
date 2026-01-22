import json
import uuid
from typing import Any, Dict


from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session
from app.services.llm_handler import LLMHandler
from app.models.exam_evaluation_final import ExamEvaluationFinal
from app.models.exam_evaluation_single_answer import ExamEvaluationSingleAnswer
from app.models.question import Question


class ExamSimulator:
    def __init__(
        self,
        rephrase_question: str,
        evaluate_student_answer: str,
        evaluate_exam: str,
    ) -> None:
        """Initializes the ExamSimulator with LLM endpoint, model, and question dataset.

        Args:
            evaluate_student_answer (str): Prompt template to evaluate student answers.
            evaluate_exam (str): Prompt template to evaluate the entire exam.
        """
        self._llm_handler = LLMHandler()
        self._prompt_evaluate_student_answer: str = evaluate_student_answer
        self._prompt_evaluate_exam: str = evaluate_exam
        self._prompt_rephrase_question: str = rephrase_question

    def _generate_unique_exam_id(self) -> str:
        """Generates a unique exam ID using UUID4.

        Returns:
            str: A unique exam identifier.
        """
        return str(uuid.uuid4())

    async def _add_data_to_db(self, data_to_add: Any) -> None:
        async with async_session() as session:
            session.add_all(data_to_add)
            await session.commit()

    async def _write_single_evaluation_to_db(
        self,
        unique_exam_id: str,
        question: str,
        student_answer: str,
        correct_answer: str,
        feedback: str,
        rating: str,
    ) -> None:
        """Writes a single evaluation entry to the database.

        Args:
            unique_exam_id (str): The unique identifier for the exam session.
            question (str): The original question asked.
            student_answer (str): The answer provided by the student.
            correct_answer (str): The correct answer for comparison.
            feedback (str): The feedback for the student's answer.
            rating (str): The rating for the student's answer.
        """
        evaluation = ExamEvaluationSingleAnswer(
            unique_exam_id=unique_exam_id,
            question=question,
            student_answer=student_answer,
            correct_answer=correct_answer,
            feedback=feedback,
            rating=rating,
        )
        await self._add_data_to_db([evaluation])


    async def evaluate_student_answer(
        self,
        unique_exam_id: str,
        question: str,
        student_answer: str,
        correct_answer: str,
        max_points: float,
        evaluate_only: bool = False,
    ) -> Dict[str, str | int | None]:

        answer_evaluation = self._llm_handler.call_llm(
            self._prompt_evaluate_student_answer.format(
                question=question,
                student_answer=student_answer,
                correct_answer=correct_answer,
                max_points=max_points,
            )
        )

        CLARIFY_TEXT = (
            "Die Antwort war noch nicht ganz vollständig. "
            "Können Sie den fehlenden Teil noch erklären?"
        )

        raw_score = float(str(answer_evaluation["overall_rating"]).strip())
        max_points = float(max_points)
        percentage = (raw_score / max_points) * 100

        followup_text = ""
        next_action = "EVALUATE_ONLY" if evaluate_only else ""

        if not evaluate_only:
            if percentage >= 90:
                next_action = "DEEPEN"
                followup_text = "Sehr gute Antwort! Vertiefungsfrage: ..."
            elif percentage < 20:
                next_action = "ADVANCE"
                followup_text = ""
            else:
                next_action = "CLARIFY"
                followup_text = CLARIFY_TEXT

        evaluation = ExamEvaluationSingleAnswer(
            unique_exam_id=unique_exam_id,
            question=question,
            student_answer=student_answer,
            correct_answer=correct_answer,
            feedback=answer_evaluation["feedback_content"],
            rating=str(raw_score),
        )
        await self._add_data_to_db([evaluation])

        return {
            "feedback": answer_evaluation["feedback_content"],
            "rating": str(raw_score),
            "next_action": next_action,
            "followup_text": followup_text,
        }

    

    def rephrase_question(self, question: str) -> Dict[str, str]:
        """Rephrases the given question using the LLM.

        Args:
            question (str): The question to be rephrased.

        Returns:
            Dict[str, str]: The rephrased question.
        """
        rephrased_answer = self._llm_handler.call_llm(
            self._prompt_rephrase_question.format(
                question=question,
            )
        )
        return rephrased_answer

    async def evaluate_the_exam(self, unique_exam_id: str) -> Dict[str, str]:
        """Evaluates the entire exam based on stored feedback and ratings.

        Args:
            unique_exam_id (str): The unique identifier for the exam session.

        Returns:
            Dict[str, str]: The final evaluation statement for the exam.
        """
        async with async_session() as session:
            result = await session.execute(
                select(
                    ExamEvaluationSingleAnswer.feedback,
                    ExamEvaluationSingleAnswer.rating,
                ).where(ExamEvaluationSingleAnswer.unique_exam_id == unique_exam_id)
            )
            rows = result.all()
        feedbacks = [entry[0] for entry in rows]
        ratings = [entry[1] for entry in rows]
        overall_feedback = "\n\n".join(feedbacks)
        overall_rating = "\n\n".join(ratings)

        final_feedback = self._llm_handler.call_llm(
            self._prompt_evaluate_exam.format(
                overall_feedback=overall_feedback, overall_rating=overall_rating
            )
        )
        if not isinstance(final_feedback["final_feedback"], str):
            final_evaluation = ExamEvaluationFinal(
                unique_exam_id=unique_exam_id,
                overall_feedback=json.dumps(final_feedback["final_feedback"]),
                overall_rating=final_feedback["final_rating"],
            )
        else:
            final_evaluation = ExamEvaluationFinal(
                unique_exam_id=unique_exam_id,
                overall_feedback=final_feedback["final_feedback"],
                overall_rating=final_feedback["final_rating"],
            )
        await self._add_data_to_db([final_evaluation])
        return final_feedback
