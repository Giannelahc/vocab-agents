
from prompts.vocabulary_identification_prompt import VocabularyIdentificationPromptBuilder


class VocabularyIdentificationAgent:
    def __init__(self, vocabulary_identify_builder: VocabularyIdentificationPromptBuilder):
        self.vocabulary_identify_builder = vocabulary_identify_builder

    async def process_text(self, text, target_language):
        return await self.vocabulary_identify_builder.identify_vocabulary(text, target_language)

    