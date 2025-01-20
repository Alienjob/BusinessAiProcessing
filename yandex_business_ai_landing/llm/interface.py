# Interface for LLM model requests.
class LLMRequestInterface:
    def answer_review(self, prompt: str) -> str:
        """ Answer review request to LLM model. """
        pass
    def describe_image(self, prompt: str, imageUrl: str) -> str:
        """ Describe image content. """
        pass
    def write_topic(self, prompt: str) -> str:
        """ Writes professional topic by image description. """
        pass
    def write_topic(self, prompt: str) -> str:
        """ Writes polite response to a review. """
        pass
