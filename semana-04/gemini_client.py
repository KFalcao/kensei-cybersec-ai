import os
import requests

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta2/models/{model}:generateText"


class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required")
        self.api_key = api_key
        self.model = model

    def generate_text(self, prompt: str, temperature: float = 0.2, max_output_tokens: int = 256) -> str:
        url = GEMINI_URL.format(model=self.model)
        payload = {
            "prompt": {
                "text": prompt
            },
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens
        }
        params = {"key": self.api_key}
        response = requests.post(url, params=params, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        # Gemini responses may include different fields depending on the model version.
        if "candidates" in data and isinstance(data["candidates"], list):
            return data["candidates"][0].get("content", "")
        if "output" in data and "text" in data["output"]:
            return data["output"]["text"]
        return data.get("response", "")

    @classmethod
    def from_env(cls):
        api_key = os.getenv("GEMINI_API_KEY")
        return cls(api_key=api_key)
