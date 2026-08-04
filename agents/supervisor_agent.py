import asyncio

from services import pos_tagger
from agents import definition_agent, grammar_agent, example_agent

class SupervisorAgent:
    def __init__(self,  
                 pos_tagger: pos_tagger.PosTaggerService, 
                 definition_agent: definition_agent.DefinitionAgent,
                 grammar_agent: grammar_agent.GrammarAgent,
                 example_agent: example_agent.ExampleAgent):
        self.pos_tagger_service = pos_tagger
        self.definition_agent = definition_agent
        self.grammar_agent = grammar_agent
        self.example_agent = example_agent

    async def run(self, word, target_languages, language_code):

        response = await self.pos_tagger_service.process_word(word, language_code)

        types = response["types"]

        tags = []

        for tag in types:
            tags.append(self.build_word_tag(word, tag, language_code, target_languages))

        result = await asyncio.gather(*tags)
        return result


    async def build_word_tag(self, word: str, tag: str, language_code: str, target_languages: list):
        tasks = [
            self.definition_agent.run(word, tag, target_languages, language_code),
            self.example_agent.run(word, tag, language_code)
        ]

        if "verb" in tag:
            tasks.append(
                self.grammar_agent.process_verb(word, language_code)
            )

        if "noun" in tag:
            tasks.append(
                self.grammar_agent.process_noun(word, language_code)
            )

        definition_data, examples, *grammar_data = await asyncio.gather(*tasks)  

        grammar = {}

        for result in grammar_data:
            grammar.update(result)

        return self.build_result(tag, definition_data, examples, grammar)

    def build_result(self, tag, definition_data, examples, grammar_data):
        
        result = {
            "part_of_speech": tag,
            **definition_data,
            **examples,
            **grammar_data
        }

        return result
