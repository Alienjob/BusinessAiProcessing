# Interface for LLM model requests.
class AiInterface:
    def request_rate(self, request: dict):
        pass
    def response_to_request(self, request: str, prompt: str) -> str:
        pass
    def generate_publication(self, imageUrl: str, description: str, prompt: str) -> str:
        pass