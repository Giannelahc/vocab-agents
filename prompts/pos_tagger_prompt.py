import json

from infrastructure.clients.llm_client import LLMClient

class PosTaggerPromptBuilder:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def getTag(self, word):
        return await self.process_word(word)

    async def process_word(self, word: str, language_detected: str):
        prompt = f"""
        Identify the grammatical types that the vocabulary item "{word}"
        can have in {language_detected}.

        Your task is ONLY to identify the grammatical categories of the
        COMPLETE vocabulary item.

        Rules:

        1. Return only grammatical or lexical types that are genuinely used
        for this vocabulary item in the given language.

        2. Consider the complete vocabulary item as one unit.
        If it contains multiple words and they function together as a
        single lexical unit, classify the complete expression.

        3. For multi-word verbal constructions such as:
        - "se rendre compte de"
        - "prendre soin de"
        - "avoir besoin de"
        classify them as "verbal_expression".

        4. Do not classify the individual words inside an expression.
        For example, do not return "verb" and "preposition" for
        "se rendre compte de". The complete item is a
        "verbal_expression".

        5. If the vocabulary item is a single verb, return "verb".

        6. If the vocabulary item can genuinely belong to multiple
        grammatical categories depending on its meaning or usage,
        return all applicable types.

        For example:
        "light" -> ["noun", "verb", "adjective"]

        7. Do not return grammatical properties such as:
        - pronominal
        - reflexive
        - transitive
        - intransitive
        - auxiliary
        These will be analyzed separately.

        8. Do not return semantic categories or meanings.

        9. Do not invent a grammatical category. If uncertain, return only
        the most reliable category.

        10. Use the following standardized type names in English:

        noun
        verb
        adjective
        adverb
        pronoun
        determiner
        preposition
        conjunction
        interjection
        numeral
        verbal_expression
        idiom
        expression
        abbreviation
        other

        11. Prefer "verbal_expression" over "expression" when the complete
            expression is centered around a verb.

        12. Return the types in lowercase.

        DO NOT use markdown.
        DO NOT use ```json.
        Return ONLY valid JSON.

        Return exactly this structure:

        {{
            "types": ["verb"]
        }}
        """

        response = await self.llm_client.complete(prompt)
        return json.loads(response.strip())