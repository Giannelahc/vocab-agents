
from prompts.grammar_prompt import GrammarPromptBuilder


class GrammarAgent:
    def __init__(self, grammar_service: GrammarPromptBuilder):
        self.grammar_service = grammar_service

    async def process_noun(self, word, tag, target_language):
        return await self.grammar_service.get_noun_grammar(word, tag, target_language)

    async def process_verb(self, word, target_language):
        return await self.grammar_service.get_verb_grammar(word, target_language)

    async def process_adjective(self, word, target_language):
        return await self.grammar_service.get_adjective_grammar(word, target_language)
    