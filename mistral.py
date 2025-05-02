from __future__ import annotations

from mistralai import Mistral
from ai_interface import AiInterface

API_KEY = 'zJUwEYPKJwuQlGYzoJs7tXlfXAbJOX9R'

answer_review_token_limit = 300

class MistralAi(AiInterface):

    def __init__(self):
        self.api_key = API_KEY

    def request_rate(self, request: dict):
        pass

    def response_to_request(self, request: dict, prompt: str) -> str | None:
        with Mistral(api_key=self.api_key) as mistral:
            try:
                res = mistral.chat.complete(
                    model="mistral-small-latest",
                    messages=[
                        {
                            "content": f"{prompt}",
                            "role": "user",
                        },
                    ],
                    max_tokens=answer_review_token_limit)

                # Check if the response contains valid data
                if res is not None and hasattr(res, 'choices') and len(res.choices) > 0:
                    # Return the content of the first choice
                    return res.choices[0].message.content
                else:
                    return None
            except Exception as e:
                print(f"Error occurred while communicating with Mistral API: {e}")
                return None

    def generate_publication(self, imageUrl: str, description: str, prompt: str) -> str:
        pass