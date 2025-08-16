from __future__ import annotations

import httpx
import base64
import requests
from mistralai import Mistral
from ai_interface import AiInterface

API_KEY = 'zJUwEYPKJwuQlGYzoJs7tXlfXAbJOX9R'

class MistralAi(AiInterface):

    def __init__(self):
        self.id = 'Mistral'
        self.api_key = API_KEY

    def getId(self) -> str:
        return self.id

    def request_rate(self, request: str, prompt: str, argument: str) -> float:
        return -1

    def describeImage(self, orgName: str, imageUrl: str, assortment: str,
                      prompt: str, argument: str, token_limit: int) -> str | None:
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
                                       f"а описание изображения формируется для продукта или услуги компании, "
                                       f"называющегося {assortment}"
                        },
                        {
                            "content": [
                                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_data}" }
                            ],
                            "role": "user"
                        }
                    ],
                    max_tokens=token_limit)
                if res is not None and hasattr(res, 'choices') and len(res.choices) > 0:
                    # Return the content of the first choice
                    return res.choices[0].message.content
                else:
                    return None
            except Exception as e:
                print(f"Error occurred while communicating with Mistral API: {e}")
                return None

    def response_to_request(self, orgName: str, request: dict, prompt: str, argument: str, char_limit: int) -> str | None:
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
                            "content": "Результирующее описание должно содержать не более " + str(char_limit) + " символов",
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
                    ])

                # Check if the response contains valid data
                if res is not None and hasattr(res, 'choices') and len(res.choices) > 0:
                    # Return the content of the first choice
                    return res.choices[0].message.content
                else:
                    return None
            except Exception as e:
                print(f"Error occurred while communicating with Mistral API: {e}")
                return None

    def generate_publication(self, orgName: str, assortment: str, description: str, imageDescription: str,
                             prompt: str, argument: str, char_limit: int) -> str | None:
        with Mistral(api_key=self.api_key, client=httpx.Client(verify=False)) as mistral:
            try:
                operatedMessages = [
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "system",
                        "content": argument
                    },
                    {
                        "role": "system",
                        "content": f"Необходимо учесть, что компания именуется как {orgName}, "
                                   f"а публикация формируется для продукта или услуги компании, "
                                   f"называющегося {assortment}"
                    },
                    {
                        "content": f"Результирующее описание должно содержать не более {char_limit} символов",
                        "role": "system",
                    },
                    {
                        "role": "user",
                        "content": f"Компания предоставила следующее описание для продукта или услуги: {description}"
                    }
                ]
                if imageDescription is not None:
                    operatedMessages.append({ "role": "user",
                        "content": f"Публикация сопровождается изображением, описание которого сформулировано как {imageDescription}"
                    })
                res = mistral.chat.complete(model = "mistral-small-latest", messages = operatedMessages)
                if res is not None and hasattr(res, 'choices') and len(res.choices) > 0:
                    # Return the content of the first choice
                    return res.choices[0].message.content
                else:
                    return None
            except Exception as e:
                print(f"Error occurred while communicating with Mistral API: {e}")
                return None
