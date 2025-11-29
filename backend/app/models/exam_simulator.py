from typing import Dict, List, Tuple
from pandas import DataFrame
from sqlite3 import Connection, Cursor

from app.core.db import get_session
from sqlalchemy import text

import uuid
import json
import requests
import pandas as pd
import sqlite3


class ExamSimulator:
    def __init__(
        self, begin_exam: str, evaluate_student_answer: str, evaluate_exam: str
    ) -> None:
        """Initializes the ExamSimulator with LLM endpoint, model, and question dataset."""
        self._llm_endpoint: str = (
            "http://catalpa-llm.fernuni-hagen.de:11434/api/generate"
        )
        self._llm_model: str = "phi4:latest"
        self._df: DataFrame = pd.read_csv("DataScienceBasics_QandA - Sheet1.csv")
        self._questions: List[str] = self._df["Question"].tolist()

        self._prompt_begin_exam: str = begin_exam
        self._prompt_evaluate_student_answer: str = evaluate_student_answer
        self._prompt_evaluate_exam: str = evaluate_exam

        get_session().execute(
            text(
                "CREATE TABLE IF NOT EXISTS exam_simulations (id INTEGER PRIMARY KEY, unique_exam_id VARCHAR, question VARCHAR, answer VARCHAR, feedback VARCHAR, rating VARCHAR)"
            )
        )
        get_session().execute(
            text(
                "CREATE TABLE IF NOT EXISTS exam_evaluations (id INTEGER PRIMARY KEY, unique_exam_id VARCHAR, overall_feedback VARCHAR, overall_rating VARCHAR)"
            )
        )

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

    def _call_llm(self, prompt: str) -> str:
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
        return self._standardize_answer(answer)

    def begin_exam(self) -> str:
        """Generates the prompt to begin the exam simulation.

        Returns:
            str: The prompt string to start the exam.
        """
        return self._call_llm(self._prompt_begin_exam.format(questions=self._questions))

    def evaluate_student_answer(self, student_answer: str, correct_answer: str) -> str:
        """Generates the prompt to evaluate the student's answer.

        Args:
            student_answer (str): The answer provided by the student.
            correct_answer (str): The correct answer for comparison.

        Returns:
            str: The prompt string to evaluate the student's answer.
        """
        return self._call_llm(
            self._prompt_evaluate_student_answer.format(
                student_answer=student_answer,
                correct_answer=correct_answer,
                questions=self._questions,
            )
        )

    def _answer_next_question_and_persist(
        self, unique_exam_id: str, question_for_student: str, question_from_db: str
    ) -> Tuple[str, str]:
        """Simulates answering the next question and persists the result in the database.

        Args:
            unique_exam_id (str): The unique identifier for the exam session.
            question (str): The question to be answered.

        Returns:
            str: The statement to be presented to the student.
        """
        payload = {
            "model": "mixtral:latest",
            "prompt": f"Du bist ein Student in einer Data Science Prüfung. Beantworte die folgende Frage: {question_for_student}. Du bist halbwegs gut vorbereitet, bitte simuliere dies.",
        }
        answer_student = requests.post(self._llm_endpoint, json=payload)
        given_answer = self._standardize_answer(answer_student)
        print("Student's Answer: ", given_answer)
        correct_answer = self._df.loc[
            self._df["Question"].str.contains(question_from_db), "Answer"
        ].values[0]
        first_answer_evaluation = self._evaluate_student_answer(
            given_answer, correct_answer
        )
        first_answer_evaluation_cleaned = self._cleanup_llm_response(
            first_answer_evaluation
        )

        get_session().execute(
            text(
                "INSERT INTO exam_simulations (unique_exam_id, question, answer, feedback, rating) VALUES (:unique_exam_id, :question, :answer, :feedback, :rating)"
            ),
            {
                "unique_exam_id": unique_exam_id,
                "question": question_for_student,
                "answer": given_answer,
                "feedback": first_answer_evaluation_cleaned["feedback_content"],
                "rating": first_answer_evaluation_cleaned["overall_rating"],
            },
        )

        self._con.commit()
        return (
            first_answer_evaluation_cleaned["statement"],
            first_answer_evaluation_cleaned["question"],
        )

    def evaluate_the_exam(self, unique_exam_id: str) -> str:
        """Evaluates the entire exam based on stored feedback and ratings.

        Args:
            unique_exam_id (str): The unique identifier for the exam session.

        Returns:
            str: The final evaluation statement for the exam.
        """
        exam_entries = (
            get_session()
            .execute(
                text(
                    "SELECT feedback, rating FROM exam_simulations WHERE unique_exam_id = :unique_exam_id"
                ),
                {"unique_exam_id": unique_exam_id},
            )
            .fetchall()
        )
        feedbacks = [entry[0] for entry in exam_entries]
        ratings = [entry[1] for entry in exam_entries]

        overall_feedback = "\n\n".join(feedbacks)
        overall_rating = max(set(ratings), key=ratings.count)  # Most common rating

        return self._call_llm(
            self._prompt_evaluate_exam.format(
                overall_feedback=overall_feedback, overall_rating=overall_rating
            )
        )
