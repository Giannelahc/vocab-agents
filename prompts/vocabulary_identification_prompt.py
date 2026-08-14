import json
from textwrap import dedent

from infrastructure.clients.llm_client import LLMClient

class VocabularyIdentificationPromptBuilder:

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def identify_vocabulary(self, text: str, language: str):
        prompt = dedent(f"""
        Analyze the following text written in {language} and identify
        meaningful vocabulary units that a language learner may want to study.

        Text:
        "{text}"

        Your task is ONLY to identify vocabulary candidates from the text.

        Do NOT provide:
        - definitions
        - translations
        - synonyms
        - conjugations
        - grammatical properties
        - explanations

        GENERAL RULES:

        1. Identify meaningful lexical units that are useful for a language
        learner.

        2. Prioritize:
        - verbs
        - verbal expressions
        - nouns
        - adjectives
        - adverbs
        - idioms
        - other meaningful lexical expressions

        3. Do NOT return every word in the sentence.

        4. Normally exclude function words such as:
        - articles
        - auxiliary verbs
        - pronouns
        - determiners
        - prepositions
        - conjunctions

        unless they are an integral part of a meaningful lexical unit.

        5. Do not return a word only because it is uncommon or appears
        important in the sentence. It must represent a meaningful
        vocabulary item that a learner could reasonably study.

        VERBS:

        6. If a verb appears conjugated, return its infinitive/base form.

        Example:
        "went" → "go"
        "mangeait" → "manger"

        7. Preserve the original form that appears in the text in the
        "text" field.

        VERBAL EXPRESSIONS:

        8. A verbal_expression must represent a recognized or conventional
        lexical unit whose meaning or grammatical behavior depends on
        the combination of its components.

        9. Only identify a verbal_expression when the combination is a
        genuine lexical construction in the language.

        10. Do NOT classify words as a verbal_expression merely because:
            - a verb is followed by another word
            - a verb is followed by an adjective
            - a verb is followed by a noun
            - a verb is followed by a prepositional phrase
            - two words frequently occur near each other

        11. For example, these are valid verbal expressions:
            - "se rendre compte de"
            - "take care of"
            - "look forward to"
            - "give up"
            - "make up one's mind"

        12. These should NOT automatically be classified as verbal expressions:
            - "eat quickly"
            - "feel happy"
            - "run fast"
            - "dwell bound"

        13. If a verb and another word can naturally function as separate
            vocabulary units, return them separately unless there is strong
            evidence that they form a fixed lexical expression.

        14. When uncertain whether several words form a verbal_expression,
            prefer separate candidates rather than creating a verbal_expression.

        15. If a verbal expression contains a conjugated verb, preserve the
            complete expression in "text", but normalize the verbal component
            when possible.

            Example:
            "je me suis rendu compte de" →
            text: "je me suis rendu compte de"
            base_form: "se rendre compte de"

        NOUNS, ADJECTIVES AND ADVERBS:

        16. Identify nouns, adjectives and adverbs when they represent
            meaningful vocabulary candidates.

        17. Preserve the original word in "text".

        18. Normalize inflected forms to their dictionary/base form when
            possible.

        19. Do not attempt to determine all possible grammatical categories
            of a word. The type returned here describes its likely use
            in the given context.

        AMBIGUOUS WORDS:

        20. If a word could belong to several grammatical categories,
            choose the category that best fits its use in the provided
            context.

        21. Do not invent additional grammatical categories or expressions
            that are not supported by the context.

        22. If the grammatical category cannot be determined reliably,
            use "other" rather than guessing.

        CANDIDATE TYPES:

        Use exactly one of:

        - "verb"
        - "verbal_expression"
        - "noun"
        - "adjective"
        - "adverb"
        - "idiom"
        - "expression"
        - "other"

        IMPORTANT:

        - The type represents the candidate's likely grammatical/lexical
        role in THIS context.
        - It is NOT a complete classification of all possible uses of
        the word.
        - Another component will later analyze the selected vocabulary
        unit in greater detail.
        - Do not use "verbal_expression" unless the combination is a
        genuine lexical unit.
        - Prefer precision over recall when identifying expressions.
        - Do not duplicate candidates.
        - Return candidates in order of relevance for a language learner.

        OUTPUT:

        Return ONLY valid JSON.
        Do NOT use markdown.
        Do NOT use ```json.

        Return exactly:

        {{
            "candidates": [
                {{
                    "text": "...",
                    "type": "...",
                    "base_form": "..."
                }}
            ]
        }}
        """)

        response_text = await self.llm_client.complete(prompt)
        return json.loads(response_text.strip())