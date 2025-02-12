from os import getenv
import re
from typing import Any
import requests


class UrlLlmProcessor:
    def __init__(self, model_id=str, temperature=float):
        self.llm_base_url = getenv("LLM_BASE_URL", "http://127.0.0.1:1234")
        self.model_id = model_id
        self.temperature = temperature

    def validate_request(self, response: Any) -> bool:
        if response.status_code == 200:
            response_dict = response.json()
            return response_dict
        else:
            raise Exception(
                f"Failed response: {response.status_code} - {response.text}"
            )

    def get_request(self, url: str) -> Any:
        response = requests.get(url)
        return self.validate_request(response)

    def post_request(self, url: str, data: dict) -> Any:
        response = requests.post(url, json=data)
        return self.validate_request(response)

    def get_model_list(self):
        return self.get_request(f"{self.llm_base_url}/v1/models")

    def get_completions_for_promt(self, prompt: str):
        payload = {
            "model": self.model_id,
            "prompt": prompt,
            "temperature": self.temperature,
        }
        response_json = self.post_request(
            f"{self.llm_base_url}/v1/completions", payload
        )
        response_text = response_json.get("choices", [{}])[0].get("text", "No response")
        return self.separate_think(response_text)

    def get_completions_for_messages(self, messages_list: list[dict[str, str]]):
        payload = {
            "model": self.model_id,
            "messages": messages_list,
            "temperature": self.temperature,
        }
        response_json = self.post_request(
            f"{self.llm_base_url}/v1/chat/completions", payload
        )
        answer_string = (
            response_json.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "No response")
        )
        return self.separate_think(answer_string)

    def separate_think(self, answer_string: str) -> dict[str, str]:
        pattern = re.compile(r"<think>(.*?)</think>", re.DOTALL)

        # Находим всё, что внутри <think></think>
        inside_matches = re.findall(pattern, answer_string)
        if inside_matches:
            inside_text = inside_matches[0]
        else:
            inside_text = ""

        outside_text = re.sub(pattern, "", answer_string, count=1)

        # if "</think>" in inside_text:
        #     inside_text = re.split(r"</think>", "", inside_text)[0]
        return {"think": inside_text, "answer": outside_text}
