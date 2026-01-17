import json
import uuid
from typing import Any, Dict, List
import pandas as pd

import requests
from sqlalchemy import select

from app.core.db import async_session
from app.models.exam_evaluation_final import ExamEvaluationFinal
from app.models.exam_evaluation_single_answer import ExamEvaluationSingleAnswer


class LLMHandler:
    def __init__(self, model: str = "phi4:latest") -> None:
        self._llm_endpoint: str = (
            "http://catalpa-llm.fernuni-hagen.de:11434/api/generate"
        )
        self._llm_model: str = model

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

    def call_llm(self, prompt: str) -> Dict[str, str]:
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


class ExamSimulator:
    def __init__(
        self,
        evaluate_student_answer: str,
        prompt_begin_exam: str,
        prompt_case_one: str,
        prompt_case_two: str,
        prompt_case_three: str,
        evaluate_exam: str,
    ) -> None:
        """Initializes the ExamSimulator with LLM endpoint, model, and question dataset.
        
        Args:
            evaluate_student_answer (str): Prompt template to evaluate student answers.
            prompt_begin_exam (str): Prompt template to begin the exam.
            prompt_case_one (str): Prompt template for case one.
            prompt_case_two (str): Prompt template for case two.
            prompt_case_three (str): Prompt template for case three.
            evaluate_exam (str): Prompt template to evaluate the entire exam.
        """
        self._llm_handler = LLMHandler()
        self._prompt_begin_exam: str = prompt_begin_exam
        self._questions: List[str] = []
        self._prompt_evaluate_student_answer: str = evaluate_student_answer
        self._prompt_case_one: str = prompt_case_one
        self._prompt_case_two: str = prompt_case_two
        self._prompt_case_three: str = prompt_case_three
        self._prompt_evaluate_exam: str = evaluate_exam

    def _generate_unique_exam_id(self) -> str:
        """Generates a unique exam ID using UUID4.

        Returns:
            str: A unique exam identifier.
        """
        return str(uuid.uuid4())

    def _case_one(
        self, question: str, student_answer: str, correct_answer: str
    ) -> Dict[str, str]:
        """Function for Case one: The student's answer is correct and complete.

        Args:
            question (str): The original question asked.
            student_answer (str): The answer provided by the student.
            correct_answer (str): The correct answer for comparison.

        Returns:
            Dict[str, str]: The follow-up question and expected answer.
        """
        answer_case_one = self._llm_handler.call_llm(
            self._prompt_case_one.format(
                question=question,
                student_answer=student_answer,
                correct_answer=correct_answer,
            )
        )
        return answer_case_one

    def _case_two(
        self, question: str, student_answer: str, correct_answer: str
    ) -> Dict[str, str]:
        """Function for Case two: The student's answer is partially correct; identify knowledge gaps.

        Args:
            question (str): The original question asked.
            student_answer (str): The answer provided by the student.
            correct_answer (str): The correct answer for comparison.

        Returns:
            Dict[str, str]: The follow-up question and expected answer.
        """
        answer_case_two = self._llm_handler.call_llm(
            self._prompt_case_two.format(
                question=question,
                student_answer=student_answer,
                correct_answer=correct_answer,
            )
        )
        return answer_case_two

    def _case_three(self, question: str) -> Dict[str, str]:
        """Function for Case three: The student does not understand the question; provide clarifications.

        Args:
            question (str): The original question asked.

        Returns:
            Dict[str, str]: The clarification and expected answer.
        """
        answer_case_three = self._llm_handler.call_llm(
            self._prompt_case_three.format(
                question=question,
            )
        )
        return answer_case_three

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
        
    def begin_exam(self) -> Dict[str, str]:
        """Generates the prompt to begin the exam simulation.

        Returns:
            Dict[str, str]: The prompt string to start the exam.
        """
        result = self._llm_handler.call_llm(
            self._prompt_begin_exam.format(questions=self._questions)
        )
        result["unique_exam_id"] = self._generate_unique_exam_id()
        return result

    async def evaluate_student_answer(
        self,
        unique_exam_id: str,
        question: str,
        student_answer: str,
        correct_answer: str,
    ) -> Dict[str, str]:
        """Generates the prompt to evaluate the student's answer.

        Args:
            unique_exam_id (str): The unique identifier for the exam session.
            question (str): The question answered by the student.
            student_answer (str): The answer provided by the student.
            correct_answer (str): The correct answer for comparison.

        Returns:
            Dict[str, str]: The prompt string to evaluate the student's answer.
        """
        answer_evaluation = self._llm_handler.call_llm(
            self._prompt_evaluate_student_answer.format(
                question=question,
                student_answer=student_answer,
                correct_answer=correct_answer,
            )
        )
        if "1" in answer_evaluation["case"] or "eins" in answer_evaluation["case"]:
            answer_case_one = self._case_one(question, student_answer, correct_answer)
            await self._write_single_evaluation_to_db(
                unique_exam_id=unique_exam_id,
                question=question,
                student_answer=student_answer,
                correct_answer=correct_answer,
                feedback=answer_case_one["feedback"],
                rating=answer_case_one["rating"],
            )
            return answer_case_one
        elif "2" in answer_evaluation["case"] or "zwei" in answer_evaluation["case"]:
            answer_case_two = self._case_two(question, student_answer, correct_answer)
            await self._write_single_evaluation_to_db(
                unique_exam_id=unique_exam_id,
                question=question,
                student_answer=student_answer,
                correct_answer=correct_answer,
                feedback=answer_case_two["feedback"],
                rating=answer_case_two["rating"],
            )
            return answer_case_two
        elif "3" in answer_evaluation["case"] or "drei" in answer_evaluation["case"]:
            answer_case_three = self._case_three(question)
            await self._write_single_evaluation_to_db(
                unique_exam_id=unique_exam_id,
                question=question,
                student_answer=student_answer,
                correct_answer=correct_answer,
                feedback="The student does not understand the question. Clarifications provided.",
                rating="Did Not Understand Question",
            )
            return answer_case_three
        return {"message": "Functionality for case one not yet implemented."}

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
