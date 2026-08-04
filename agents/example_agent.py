from services.example_service import ExampleService

class ExampleAgent:
    def __init__(self, example_service: ExampleService):
        self.example_service = example_service

    def run(self, word, tag, language_detected):
        examples = self.generate_examples(word, tag, language_detected)
        return examples##["examples"]

    def generate_examples(self, word: str, tag: str, language_detected: str) -> dict:
        return self.example_service.get_examples(word, tag, language_detected)