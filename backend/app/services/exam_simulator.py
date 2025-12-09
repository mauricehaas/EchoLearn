import json
import uuid
from typing import Any, Dict

import requests
from sqlalchemy import select

from app.core.db import async_session
from app.models.exam_evaluation_final import ExamEvaluationFinal
from app.models.exam_evaluation_single_answer import ExamEvaluationSingleAnswer


class ExamSimulator:
    def __init__(
        self,
        evaluate_student_answer: str,
        evaluate_exam: str,
    ) -> None:
        """Initializes the ExamSimulator with LLM endpoint, model, and question dataset."""
        self._llm_endpoint: str = (
            "http://catalpa-llm.fernuni-hagen.de:11434/api/generate"
        )
        self._llm_model: str = "phi4:latest"
        self._prompt_evaluate_student_answer: str = evaluate_student_answer
        self._prompt_evaluate_exam: str = evaluate_exam

    def _standardize_answer(self, answer: str) -> str:
        """Function to extract the answer parts returned as a string of JSONs from the LLM.

        Args:
            answer (str): String of JSONs coming from the LLM

        Returns:
            str: Extracted and concatenated response text from the JSONs
        """
        texts = answer.text.split("\n")

        texts_json = [json.loads(t) for t in texts if t.strip() != ""]
        text = "".join([t["response"] for t in texts_json])
        return text

    def _generate_unique_exam_id(self) -> str:
        """Generates a unique exam ID using UUID4.

        Returns:
            str: A unique exam identifier.
        """
        return str(uuid.uuid4())

    def _cleanup_llm_response(self, response: str) -> Dict[str, str]:
        """Cleans up the LLM response to extract the JSON content.

        Args:
            response (str): The raw response from the LLM.

        Returns:
            Dict[str, str]: The cleaned JSON content as a dictionary.
        """
        start_idx = response.find("```json")
        end_idx = response.rfind("```")

        return json.loads(response[start_idx + 7 : end_idx].strip())

    def _call_llm(self, prompt: str) -> Dict[str, str]:
        """Calls the LLM endpoint with the given prompt.

        Args:
            prompt (str): The prompt to send to the LLM.

        Returns:
            str: The standardized answer from the LLM.
        """
        payload = {
            "model": self._llm_model,
            "prompt": prompt,
        }

        answer = requests.post(self._llm_endpoint, json=payload)
        answer_strd = self._standardize_answer(answer)
        return self._cleanup_llm_response(answer_strd)

    async def _add_data_to_db(self, data_to_add: Any) -> None:
        async with async_session() as session:
            session.add_all(data_to_add)
            await session.commit()

    async def evaluate_student_answer(
        self,
        unique_exam_id: str,
        student_answer: str,
        correct_answer: str,
    ) -> Dict[str, str]:
        """Generates the prompt to evaluate the student's answer.

        Args:
            unique_exam_id (str): The unique identifier for the exam session.
            student_answer (str): The answer provided by the student.
            correct_answer (str): The correct answer for comparison.

        Returns:
            Dict[str, str]: The prompt string to evaluate the student's answer.
        """
        answer_evaluation = self._call_llm(
            self._prompt_evaluate_student_answer.format(
                student_answer=student_answer,
                correct_answer=correct_answer,
            )
        )
        evaluation = ExamEvaluationSingleAnswer(
            unique_exam_id=unique_exam_id,
            student_answer=student_answer,
            correct_answer=correct_answer,
            feedback=answer_evaluation["feedback_content"],
            rating=answer_evaluation["overall_rating"],
        )
        await self._add_data_to_db([evaluation])
        return answer_evaluation

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
        overall_rating = "\n\n".join(ratings)  # Most common rating

        final_feedback = self._call_llm(
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
