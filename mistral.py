from __future__ import annotations

import httpx
import base64
import requests
from mistralai import Mistral
from ai_interface import AiInterface

API_KEY = 'zJUwEYPKJwuQlGYzoJs7tXlfXAbJOX9R'

answer_review_token_limit = 300
describe_image_token_limit = 1000

class MistralAi(AiInterface):

    def __init__(self):
        self.id = 'Mistral'
        self.api_key = API_KEY

    def getId(self) -> str:
        return self.id

    def request_rate(self, request: dict):
        pass

    def response_to_request(self, orgName: str, request: dict, prompt: str, argument: str) -> str | None:
        with Mistral(api_key=self.api_key, client=httpx.Client(verify=False)) as mistral:
            try:
                res = mistral.chat.complete(
                    model="mistral-small-latest",
                    messages=[
                        {
                            "content": prompt,
                            "role": "system",
                        },
                        {
                            "content": argument,
                            "role": "system",
                        },
                        {
                            "role": "system",
                            "content": f"Необходимо учесть, что компания именуется как {orgName}"
                        },
                        {
                            "content": f"Пользователь услуг направил в компанию запрос следующего содержания: {request}",
                            "role": "user",
                        }
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

    def generate_publication(self, imageUrl: str, orgName: str, assortment: str,
                             description: str, prompt: str, argument: str) -> str | None:
        with Mistral(api_key=self.api_key, client=httpx.Client(verify=False)) as mistral:
            try:
                response = requests.get(imageUrl, stream=True)
                image_data = base64.b64encode(response.content).decode('utf-8')
                res = mistral.chat.complete(
                    model="pixtral-12b-2409",
                    messages=[
                        {
                            "role": "system",
                            "content": prompt
                        },
                        {
                            "content": argument,
                            "role": "system",
                        },
                        {
                            "role": "system",
                            "content": f"Необходимо учесть, что компания именуется как {orgName}, "
                                       f"а описание формируется для продукта или услуги компании, "
                                       f"называющегося {assortment}"
                        },
                        {
                            "role": "user",
                            "content": description
                        },
                        {
                            "content": [
                                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_data}" }
                            ],
                            "role": "user"
                        }
                    ],
                    max_tokens=describe_image_token_limit)
                if res is not None and hasattr(res, 'choices') and len(res.choices) > 0:
                    # Return the content of the first choice
                    return res.choices[0].message.content
                else:
                    return None
            except Exception as e:
                print(f"Error occurred while communicating with Mistral API: {e}")
                return None
