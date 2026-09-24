import json

from infrastructure.clients.llm_client import LLMClient

class PosTaggerPromptBuilder:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def getTag(self, word):
        return await self.process_word(word)

    async def process_word(self, word: str, language_detected: str):
        prompt = f"""
        Analyze the vocabulary item "{word}" in {language_detected}.

        Your task has TWO steps:

        1. Determine whether the COMPLETE input is a valid lexical unit.
        2. If it is a valid lexical unit, identify all grammatical types that
        the COMPLETE item can genuinely have in the given language.

        IMPORTANT:
        Do not modify, correct, split, merge, or reinterpret the user's input.
        Analyze exactly what the user provided.

        STEP 1 — DETERMINE THE INPUT TYPE

        Classify the complete input into exactly one of these statuses:

        - "valid"
        The complete input is a recognized lexical unit.

        - "multiple_words"
        The input contains multiple independent words that do not form
        an established lexical unit.

        - "uncertain"
        It is unclear whether the complete input is a recognized lexical
        unit or its grammatical classification cannot be determined reliably.

        A lexical unit can be:
        - a single word
        - a phrasal verb
        - a fixed or established multi-word expression
        - an idiom
        - another established lexicalized expression

        A sequence of words is NOT automatically a lexical unit just because
        the words commonly appear together.

        For example:

        "paint" -> valid
        "take care of" -> valid
        "look after" -> valid
        "se rendre compte de" -> valid

        STEP 2 — IDENTIFY GRAMMATICAL TYPES

        Only perform grammatical type classification when the status is "valid".

        If the input is a SINGLE WORD:
        return every grammatical category that the word genuinely has
        in the given language.

        Examples:

        "light" -> ["noun", "verb", "adjective"]

        "bound" -> return all genuinely applicable grammatical types
        for the word "bound" in the given language.

        If the input is a MULTI-WORD LEXICAL UNIT:
        classify the COMPLETE expression, not its individual words.

        Examples:

        "take care of" -> ["verbal_expression"]

        "look after" -> ["verbal_expression"]

        "se rendre compte de" -> ["verbal_expression"]

        "prendre soin de" -> ["verbal_expression"]

        "avoir besoin de" -> ["verbal_expression"]

        Do NOT return the individual grammatical categories of the words
        inside a recognized expression.

        For example, do NOT return:
        ["verb", "preposition"]

        for "se rendre compte de".

        The complete item is a "verbal_expression".

        IMPORTANT DISTINCTION:

        The presence of a verb inside a multi-word input is NOT sufficient
        to classify the complete input as "verbal_expression".

        A multi-word input should only receive "verbal_expression" when
        the COMPLETE sequence is an established lexicalized verbal unit.

        Distinguish between:

        - established lexical units
        - ordinary combinations of independent words
        - accidental sequences of words

        Only an established lexical unit should receive a grammatical type
        such as "verbal_expression", "idiom", or "expression".

        GRAMMATICAL TYPES

        Use ONLY these standardized type names:

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

        If the complete valid lexical unit genuinely belongs to multiple
        grammatical categories depending on its meaning or usage, return all
        applicable types.

        Example:

        "light" -> ["noun", "verb", "adjective"]

        For multi-word expressions, do not return the grammatical categories
        of individual words.

        GRAMMATICAL PROPERTIES

        Do NOT return grammatical properties such as:

        - pronominal
        - reflexive
        - transitive
        - intransitive
        - auxiliary

        These will be analyzed separately.

        Do NOT return semantic categories or meanings.

        Do NOT invent a grammatical category.

        If the input is "multiple_words" or "uncertain", return an empty
        types array.

        TYPE DEFINITIONS

        - "verbal_expression":
        An established multi-word lexical unit centered around a verb,
        such as a phrasal verb or established verbal construction.

        - "idiom":
        An established multi-word expression whose meaning is
        non-compositional or idiomatic.

        - "expression":
        An established multi-word lexicalized expression that is neither
        specifically a verbal expression nor an idiom.

        Prefer "verbal_expression" over "expression" when the complete
        lexical unit is centered around a verb.

        Use "idiom" only when the expression has an established
        non-compositional or idiomatic meaning.

        OUTPUT

        Return ONLY valid JSON.
        Do NOT use markdown.
        Do NOT use ```json.

        Return exactly this structure:

        {{
            "status": "valid",
            "types": ["verb"]
        }}

        The "status" field MUST contain exactly one of:

        "valid"
        "multiple_words"
        "uncertain"

        for "valid" status, the "types" field MUST contain a JSON array of all
        applicable grammatical types for the complete lexical unit. 
        For "multiple_words" or "uncertain" status, the "types" field MUST be an empty array.

        The "types" field MUST contain a JSON array.

        Examples:

        Input: "take care of"

        {{
            "status": "valid",
            "types": ["verbal_expression"]
        }}

        Input: "light"

        {{
            "status": "valid",
            "types": ["noun", "verb", "adjective"]
        }}
        """

        response = await self.llm_client.complete(prompt)
        return json.loads(response.strip())