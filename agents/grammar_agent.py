
from prompts.grammar_service import GrammarService


class GrammarAgent:
    def __init__(self, grammar_service: GrammarService):
        self.grammar_service = grammar_service

    async def process_noun(self, word, tag, target_language):
        return await self.grammar_service.get_gender(word, tag, target_language)

    async def process_verb(self, word, target_language):
        return await self.grammar_service.get_conjugation(word, target_language)
    