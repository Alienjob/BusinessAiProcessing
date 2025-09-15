from __future__ import annotations

import base64
import uuid
import time
import re

import requests
import urllib3

import environment
from ai_interface import AiInterface

# Disable SSL warnings for GigaChat API
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GigaChatAi(AiInterface):

    def __init__(self):
        self.id = 'GigaChat'
        env = environment.Environment('business-ai-service')
        self.auth_key = env.get('python.gigachat-auth-key')
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.access_token = None
        self.token_expires_at = None
        
        # Model tiers (high -> low performance)
        self.text_tiers = [
            "GigaChat-Pro",
            "GigaChat",
            "GigaChat-Max"
        ]
        
        # Vision models for image description
        self.vision_tiers = [
            "GigaChat-Pro",
            "GigaChat",
            "GigaChat-Max"
        ]

    # Helper to pick model by kind and tier offset (0=pro, 1=standard, 2=max)
    def _pick_model(self, kind: str, lower_tier: int) -> str:
        tiers = self.text_tiers if kind == "text" else self.vision_tiers
        index = max(0, min(lower_tier, 2))
        return tiers[index]

    def _get_auth_token(self) -> bool:
        """Get or refresh authentication token"""
        if self.access_token and self.token_expires_at:
            # Check if token is still valid (with 5-minute buffer)
            if time.time() < (self.token_expires_at / 1000 - 300):
                return True
        
        if not self.auth_key:
            print("GigaChat authentication key not configured")
            return False
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {self.auth_key}"
        }
        
        try:
            response = requests.post(
                self.auth_url,
                headers=headers,
                data={"scope": "GIGACHAT_API_PERS"},
                verify=False
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            self.token_expires_at = token_data.get("expires_at")
            
            return self.access_token is not None
        except Exception as e:
            print(f"GigaChat authentication failed: {e}")
            return False

    def _chat_completion(self, messages: list, model: str, max_tokens: int = None) -> str | None:
        """Generic chat completion method"""
        if not self._get_auth_token():
            return None
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": 0.7
        }
        
        if max_tokens:
            data["max_tokens"] = max_tokens
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                verify=False
            )
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            return None
            
        except Exception as e:
            print(f"GigaChat API error: {e}")
            return None

    def getId(self) -> str:
        return self.id

    def request_rate(self, request: str, prompt: str) -> float:
        model = self._pick_model("text", 0)
        
        messages = [
            {"role": "system", "content": prompt},
            {
                "role": "system",
                "content": "Верните только числовое значение от 1 до 10 без дополнительных объяснений."
            },
            {"role": "user", "content": request}
        ]
        
        result = self._chat_completion(messages, model, 10)
        
        if result:
            try:
                # Extract numeric value
                match = re.search(r'\d+(?:\.\d+)?', result)
                if match:
                    rating = float(match.group())
                    return max(1.0, min(10.0, rating))  # Clamp to valid range
            except:
                pass
        
        return 5.0  # Default neutral rating

    def response_to_request(self, orgName: str, request: dict, prompt: str, char_limit: int, lower_tier: int = 0) -> str | None:
        model = self._pick_model("text", lower_tier)
        
        messages = [
            {"role": "system", "content": prompt},
            {
                "role": "system",
                "content": f"Результирующее описание должно содержать не более {char_limit} символов"
            },
            {
                "role": "system",
                "content": f"Необходимо учесть, что компания именуется как {orgName}"
            },
            {
                "role": "user",
                "content": f"Пользователь услуг направил в компанию запрос следующего содержания: {request}"
            }
        ]
        
        result = self._chat_completion(messages, model, char_limit * 2)
        
        if result is None and lower_tier < 2:
            print(f"Retrying response_to_request with lower tier: {lower_tier + 1}")
            return self.response_to_request(orgName, request, prompt, char_limit, lower_tier + 1)
        
        return result

    def generate_publication(self, orgName: str, assortment: str, description: str,
                           imageDescription: str, prompt: str, char_limit: int, lower_tier: int = 0) -> str | None:
        model = self._pick_model("text", lower_tier)
        
        messages = [
            {"role": "system", "content": prompt},
            {
                "role": "system",
                "content": f"Необходимо учесть, что компания именуется как {orgName}, "
                          f"а публикация формируется для продукта или услуги компании, "
                          f"называющегося {assortment}"
            },
            {
                "role": "system",
                "content": f"Результирующее описание должно содержать не более {char_limit} символов"
            },
            {
                "role": "user",
                "content": f"Компания предоставила следующее описание для продукта или услуги: {description}"
            }
        ]
        
        if imageDescription is not None:
            messages.append({
                "role": "user",
                "content": f"Публикация сопровождается изображением, описание которого сформулировано как {imageDescription}"
            })
        
        result = self._chat_completion(messages, model, char_limit * 2)
        
        if result is None and lower_tier < 2:
            print(f"Retrying generate_publication with lower tier: {lower_tier + 1}")
            return self.generate_publication(orgName, assortment, description, imageDescription, prompt, char_limit, lower_tier + 1)
        
        return result

    def describeImage(self, orgName: str, imageUrl: str, assortment: str,
                     prompt: str, token_limit: int, lower_tier: int = 0) -> str | None:
        model = self._pick_model("vision", lower_tier)
        
        try:
            # Download and encode image
            response = requests.get(imageUrl, stream=True)
            image_data = base64.b64encode(response.content).decode('utf-8')
            
            messages = [
                {"role": "system", "content": prompt},
                {
                    "role": "system",
                    "content": f"Необходимо учесть, что компания именуется как {orgName}, "
                              f"а описание изображения формируется для продукта или услуги компании, "
                              f"называющегося {assortment}"
                },
                {
                    "role": "system",
                    "content": f"Результирующее описание должно содержать не более {token_limit} символов"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{image_data}"
                        }
                    ]
                }
            ]
            
            result = self._chat_completion(messages, model, token_limit)
            
            if result is None and lower_tier < 2:
                print(f"Retrying describeImage with lower tier: {lower_tier + 1}")
                return self.describeImage(orgName, imageUrl, assortment, prompt, token_limit, lower_tier + 1)
            
            return result
            
        except Exception as e:
            if lower_tier < 2:
                print(f"Retrying describeImage with lower tier: {lower_tier + 1}")
                return self.describeImage(orgName, imageUrl, assortment, prompt, token_limit, lower_tier + 1)
            print(f"Error processing image for GigaChat: {e}")
            return None