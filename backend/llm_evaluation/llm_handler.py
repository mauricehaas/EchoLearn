import json
from typing import Dict
import requests


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
