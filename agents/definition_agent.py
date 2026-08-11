from prompts.definition_prompt import DefinitionPromptBuilder

class DefinitionAgent:
    def __init__(self, dictionary_service: DefinitionPromptBuilder):
        self.dictionary_service = dictionary_service

    def run(self, word, tag, target_languages, language_detected):
        definitions = self.generate_definitions(word, tag, target_languages, language_detected)
        return definitions

    def generate_definitions(self, word: str, tag: str, target_languages, language_detected: str) -> dict:
        return self.dictionary_service.get_definition(word, tag, target_languages, language_detected)