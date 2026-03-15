import json
import uuid
from typing import Any, Dict

from sqlalchemy import select

from app.core.db import async_session
from app.models.exam_evaluation_final import ExamEvaluationFinal
from app.models.exam_evaluation_single_answer import ExamEvaluationSingleAnswer
from app.services.llm_handler import LLMHandler


class ExamSimulator:
    def __init__(
        self,
        rephrase_question: str,
        evaluate_student_answer: str,
        evaluate_exam: str,
        next_question: str,
        clarify: str,
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
        self._prompt_next_question: str = next_question
        self._prompt_clarify: str = clarify

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

    async def _add_single_data_to_db(self, data_to_add):
        async with async_session() as session:
            session.add(data_to_add)
            await session.flush()
            obj_id = data_to_add.id
            await session.commit()
            return obj_id

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
        max_points: int,
        question_type: str,
        evaluate_only: bool = False,
        parent_id: int = 0,
    ) -> Dict[str, str | int | None]:
        """Evaluates a student's answer to a question and provides feedback, rating, and next steps.

        Args:
            unique_exam_id (str): The unique identifier for the exam session.
            question (str): The original question asked.
            student_answer (str): The answer provided by the student.
            correct_answer (str): The correct answer for comparison.
            max_points (int): The maximum points for the question.
            question_type (str): The type of the question (e.g., "multiple_choice", "open_ended").
            evaluate_only (bool, optional): Whether to only evaluate without suggesting next steps. Defaults to False.
            parent_id (int, optional): The ID of the parent evaluation entry for follow-up questions. Defaults to 0.

        Returns:
            Dict[str, str | int | None]: A dictionary containing feedback, rating, next action, and follow-up information.
        """

        answer_evaluation = self._llm_handler.call_llm(
            self._prompt_evaluate_student_answer.format(
                question=question,
                student_answer=student_answer,
                correct_answer=correct_answer,
                max_points=max_points,
            )
        )

        raw_score = float(str(answer_evaluation["overall_rating"]).strip())
        max_points = float(max_points)
        percentage = (raw_score / max_points) * 100

        followup_text = ""
        next_answer = ""
        next_action = "EVALUATE_ONLY" if evaluate_only else ""

        if not evaluate_only:
            if percentage >= 80:
                next_action = "DEEPEN"
                next_question = self._llm_handler.call_llm(
                    self._prompt_next_question.format(
                        question=question,
                        student_answer=student_answer,
                        correct_answer=correct_answer,
                    )
                )
                followup_text = next_question["question"]
                next_answer = next_question["answer"]
            elif percentage < 50:
                next_action = "ADVANCE"
                followup_text = ""
            else:
                next_action = "CLARIFY"
                feedback = self._llm_handler.call_llm(
                    self._prompt_clarify.format(
                        question=question,
                        student_answer=student_answer,
                        correct_answer=correct_answer,
                    )
                )
                followup_text = feedback["hint"]

        evaluation = ExamEvaluationSingleAnswer(
            unique_exam_id=unique_exam_id,
            question=question,
            question_type=question_type,
            student_answer=student_answer,
            correct_answer=correct_answer,
            feedback=answer_evaluation["feedback_content"],
            rating=str(raw_score),
            parent_id=parent_id,
            max_points=str(max_points),
        )
        answer_id = await self._add_single_data_to_db(evaluation)

        if next_action == "DEEPEN":
            return {
                "feedback": answer_evaluation["feedback_content"],
                "rating": str(raw_score),
                "next_action": next_action,
                "next_max_points": 5,
                "next_answer": next_answer,
                "followup_text": followup_text,
                "answer_id": answer_id,
            }
        else:
            return {
                "feedback": answer_evaluation["feedback_content"],
                "rating": str(raw_score),
                "next_action": next_action,
                "followup_text": followup_text,
                "answer_id": answer_id,
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
            )
        else:
            final_evaluation = ExamEvaluationFinal(
                unique_exam_id=unique_exam_id,
                overall_feedback=final_feedback["final_feedback"],
            )
        await self._add_data_to_db([final_evaluation])
        return final_feedback
