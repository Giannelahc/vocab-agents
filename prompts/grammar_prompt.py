import json
from textwrap import dedent

from infrastructure.clients.llm_client import LLMClient

class GrammarPromptBuilder:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def get_noun_grammar(self, word, tag, target_language):
        prompt = dedent(f"""
        Analyze the grammatical information of '{word}' as a {tag}
        in {target_language}.

        Return both:
        1. The grammatical gender.
        2. The relevant grammatical properties of the noun.

        GENDER:

        - Return "masculine" or "feminine" when the noun has grammatical gender.
        - If the language does not assign grammatical gender to this noun,
        return null.

        PROPERTIES:

        Determine the following properties:

        - countable: true if the noun can refer to individual countable entities
        and can normally be used with a number.
        - plural_form: the standard plural form of the noun, if applicable.

        IMPORTANT:

        - Analyze the word specifically as a noun in {target_language}.
        - Do not infer gender from the meaning of the word.
        - Use the grammatical rules of the target language.
        - Do not confuse grammatical gender with biological sex.
        - Some nouns can have different meanings with different genders.
        Analyze the relevant/common meaning of the given vocabulary item.
        - Do not provide definitions, translations, synonyms, examples,
        or conjugations.
        - If a property does not apply, return null.
        - Return all field names in English.

        DO NOT use markdown.
        DO NOT use ```json.
        Return ONLY valid JSON.

        Return exactly this structure:

        {{
            "gender": null,
            "properties": {{
                "countable": null,
                "plural_form": null
            }}
        }}
        """)

        response_text = await self.llm_client.complete(prompt)
        return json.loads(response_text.strip())
    
    async def get_verb_grammar(self, word, target_language):
        prompt = dedent(f"""
        Analyze the grammatical information of the verb '{word}' in
        {target_language}.

        Return both:
        1. The requested conjugation.
        2. The grammatical properties of the verb.

        CONJUGATION:

        Provide:
        - Present tense: first person singular, first person plural,
        and third person plural.
        - Past participle.
        - Future tense: first person singular, first person plural,
        and third person plural.

        Use the appropriate equivalent forms for the target language.
        If a requested grammatical form does not exist in the target language,
        return null for that form.

        GRAMMATICAL PROPERTIES:

        Analyze the verb and determine:

        - base_verb: infinitive or dictionary/base form.
        - pronominal: true if the verb is genuinely pronominal.
        - reflexive: true if the construction expresses a reflexive action.
        - reciprocal: true if the construction expresses a reciprocal action.
        - transitive: true if the verb can take a direct object.
        - intransitive: true if the verb can be used without a direct object.
        - preposition: the preposition that is an integral part of the
        construction, if applicable.

        IMPORTANT:

        - Analyze the complete vocabulary item as a unit.
        - Do not confuse pronominal, reflexive, reciprocal, transitive,
        or intransitive with the grammatical type of the word.
        - A verb may be both transitive and intransitive.
        - Do not invent properties.
        - If a property does not apply, return false for boolean properties
        and null for string properties.
        - Do not provide definitions, translations, synonyms, or examples.
        - Return all field names in English.

        DO NOT use markdown.
        DO NOT use ```json.
        Return ONLY valid JSON.

        Return exactly this structure:

        {{
            "conjugation": {{
                "present": {{
                    "first_singular": "...",
                    "first_plural": "...",
                    "third_plural": "..."
                }},
                "past_participle": "...",
                "future": {{
                    "first_singular": "...",
                    "first_plural": "...",
                    "third_plural": "..."
                }}
            }},
            "properties": {{
                "base_verb": "...",
                "pronominal": false,
                "reflexive": false,
                "reciprocal": false,
                "transitive": false,
                "intransitive": false,
                "preposition": null
            }}
        }}
        """)

        response_text = await self.llm_client.complete(prompt)
        return json.loads(response_text.strip())


    async def get_adjective_grammar(self, word, tag, target_language):
        prompt = dedent(f"""
        Analyze the grammatical information of '{word}' as an {tag}
        in {target_language}.

        Return both:
        1. The grammatical gender, if applicable.
        2. The relevant grammatical properties of the adjective.

        GENDER:

        - Return "masculine" or "feminine" when the adjective has grammatical
        gender in the target language.
        - If grammatical gender does not apply, return null.

        PROPERTIES:

        Determine the following properties:

        - comparative: the standard comparative form of the adjective, if
        the language has a specific comparative form. Otherwise return null.
        - superlative: the standard superlative form of the adjective, if
        applicable. Otherwise return null.
        - position: indicate where the adjective is normally placed relative
        to the noun. Use one of:
            "before_noun"
            "after_noun"
            "before_or_after_noun"

        IMPORTANT:

        - Analyze the word specifically as an adjective in {target_language}.
        - Do not provide definitions, translations, synonyms, examples,
        or conjugations.
        - Do not invent comparative or superlative forms.
        - If the adjective does not normally have a comparative or superlative
        form, return null.
        - Use the standard/common grammatical usage of the target language.
        - Return all field names in English.

        DO NOT use markdown.
        DO NOT use ```json.
        Return ONLY valid JSON.

        Return exactly this structure:

        {{
            "gender": null,
            "properties": {{
                "comparative": null,
                "superlative": null,
                "position": null
            }}
        }}
        """)

        response_text = await self.llm_client.complete(prompt)
        return json.loads(response_text.strip())