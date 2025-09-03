from __future__ import annotations

import base64

import httpx
import requests
from mistralai import Mistral

import environment
from ai_interface import AiInterface


class MistralAi(AiInterface):

    def __init__(self):
        self.id = 'Mistral'
        env = environment.Environment('business-ai-service')
        self.api_key = env.get('python.mistral-key')

    def getId(self) -> str:
        return self.id

    def request_rate(self, request: str, prompt: str) -> float:
        return -1

    def describeImage(self, orgName: str, imageUrl: str, assortment: str,
                      prompt: str, token_limit: int) -> str | None:
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
                            "role": "system",
                            "content": f"Необходимо учесть, что компания именуется как {orgName}, "
                                       f"а описание изображения формируется для продукта или услуги компании, "
                                       f"называющегося {assortment}"
                        },
                        {
                            "content": "Результирующее описание должно содержать не более " + str(token_limit) + " символов",
                            "role": "system",
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

    def response_to_request(self, orgName: str, request: dict, prompt: str, char_limit: int) -> str | None:
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

    def generate_publication(self, orgName: str, assortment: str, description: str,
                             imageDescription: str, prompt: str, char_limit: int) -> str | None:
        with Mistral(api_key=self.api_key, client=httpx.Client(verify=False)) as mistral:
            try:
                operatedMessages = [
                    {
                        "role": "system",
                        "content": prompt
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
