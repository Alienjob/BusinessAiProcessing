import os
import base64
import requests
from mistralai import Mistral
from yandex_business_ai_landing.llm.interface import LLMRequestInterface
from flask import current_app

API_KEY = 'zJUwEYPKJwuQlGYzoJs7tXlfXAbJOX9R'

answer_review_token_limit = 300
describe_image_token_limit = 5000
write_topic_token_limit = 3000
write_issue_response_token_limit = 3000

class MistralRequest(LLMRequestInterface):
    """ Answer review request to LLM model. """
    def __init__(self):
        self.api_key = API_KEY

    def answer_review(self, prompt: str) -> str:
        with Mistral(api_key=self.api_key) as s:
            try:
                res = s.chat.complete(
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
                    return "No response from Mistral API"
            except Exception as e:
                print(f"Error occurred while communicating with Mistral API: {e}")
                return "Error occurred while communicating with Mistral API"

    def describe_image(self, prompt: str, image_url: str) -> str:
        with Mistral(api_key=self.api_key) as s:
            try:
                # Read the image from the file system
                filename = os.path.basename(image_url)
                image_path = os.path.join(current_app.root_path, 'uploads', 'photos', filename)
                with open(image_path, 'rb') as f:
                    image_data = f.read()

                encoded_image = base64.b64encode(image_data).decode('utf-8')

                res = s.chat.complete(
                    model="pixtral-12b-2409", 
                    messages=[
                        {
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded_image}" }
                            ],
                            "role": "user",
                        },
                    ],
                    max_tokens=describe_image_token_limit)

                # Check if the response contains valid data
                if res is not None and hasattr(res, 'choices') and len(res.choices) > 0:
                    # Return the content of the first choice
                    return res.choices[0].message.content
                else:
                    return "No response from Mistral API"
            except Exception as e:
                print(f"Error occurred while communicating with Mistral API: {e}")
                return "Error occurred while communicating with Mistral API"

    def write_topic(self, prompt: str) -> str:
        with Mistral(api_key=self.api_key) as s:
            try:
                res = s.chat.complete(
                    model="mistral-small-latest", 
                    messages=[
                        {
                            "content": f"{prompt}",
                            "role": "user",
                        },
                    ],
                    max_tokens=write_topic_token_limit)

                # Check if the response contains valid data
                if res is not None and hasattr(res, 'choices') and len(res.choices) > 0:
                    # Return the content of the first choice
                    return res.choices[0].message.content
                else:
                    return "No response from Mistral API"
            except Exception as e:
                print(f"Error occurred while communicating with Mistral API: {e}")
                return "Error occurred while communicating with Mistral API"

    def write_issue_response(self, prompt: str) -> str:
        with Mistral(api_key=self.api_key) as s:
            try:
                res = s.chat.complete(
                    model="mistral-small-latest", 
                    messages=[
                        {
                            "content": f"{prompt}",
                            "role": "user",
                        },
                    ],
                    max_tokens=write_topic_token_limit)

                # Check if the response contains valid data
                if res is not None and hasattr(res, 'choices') and len(res.choices) > 0:
                    # Return the content of the first choice
                    return res.choices[0].message.content
                else:
                    return "No response from Mistral API"
            except Exception as e:
                print(f"Error occurred while communicating with Mistral API: {e}")
                return "Error occurred while communicating with Mistral API"
