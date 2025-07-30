# Interface for LLM model requests.
import enum

class AiInterface:
    def getId(self) -> str:
        pass
    def request_rate(self, request: dict):
        pass
    def response_to_request(self, orgName: str, request: str, prompt: str, argument: str) -> str:
        pass
    def generate_publication(self, imageUrl: str, orgName: str, assortment: str, description: str, prompt: str, argument: str) -> str:
        pass

@enum.unique
class AiTarget(enum.Enum):
    publication = 0
    response = 1
