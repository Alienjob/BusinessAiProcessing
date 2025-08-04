# Interface for LLM model requests.
import enum

class AiInterface:
    def getId(self) -> str:
        pass
    def request_rate(self, request: dict):
        pass
    def response_to_request(self, orgName: str, request: str, prompt: str, argument: str, char_limit: int) -> str:
        pass
    def generate_publication(self, orgName: str, assortment: str, description: str, imageDescription: str, prompt: str, argument: str, char_limit: int) -> str:
        pass
    def describeImage(self, orgName: str, imageUrl: str, assortment: str, prompt: str, argument: str, token_limit: int) -> str:
        pass

@enum.unique
class AiTarget(enum.Enum):
    publication = 0
    response = 1
