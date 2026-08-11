import json
from textwrap import dedent

from infrastructure.clients.llm_client import LLMClient

class ExercisePromptBuilder:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def generate_definition_exercise(self, word: str, tag: str, target_language: str, correct_definition: str):
        prompt = dedent(f"""
        Generate a multiple-choice definition exercise for the word '{word}' as a {tag} in {target_language}.
        Provide 4 options, including the correct definition '{correct_definition}' shortened and 3 distractors.
        In the correct_option field, specify the index of the correct option (0, 1, 2, or 3).
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
            "question": "What is the definition of '{word}' as a {tag} in {target_language}?",
            "options": ["..", "..", "..", ".."],
            "correct_option": ""
        }}
        """)
        response_text = await self.llm_client.complete(prompt)
        response = json.loads(response_text.strip())
        return response

    async def generate_multiple_choice_translation_exercise(self, word: str, tag: str, native_language: str, correct_translation: str):
        prompt = dedent(f"""
        Generate a multiple-choice translation exercise for the word '{word}' as a {tag} in {native_language}.
        Provide 4 options, including the correct translation '{correct_translation}' and 3 distractors.
        In the correct_option field, specify the index of the correct option (0, 1, 2, or 3).
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
            "question": "What is the translation of '{word}' in {native_language}?",
            "options": ["..", "..", "..", ".."],
            "correct_option": ""
        }}
        """)
        response_text = await self.llm_client.complete(prompt)
        response = json.loads(response_text.strip())
        return response

    async def generate_fill_in_the_blank_exercise(self, word: str, tag: str, target_language: str, synonym: str):
        prompt = dedent(f"""
        Generate a fill-in-the-blank sentence in the question field for the word '{word}' as a {tag} in {target_language}.
        Create a natural sentence where the blank can be correctly completed with the synonym '{synonym}'.
        
        Provide 4 options:
        - the correct synonym '{synonym}'
        - 3 plausible distractors
        
        The sentence must test the meaning or usage of the word '{word}', not simply repeat the word itself.
        In the correct_option field, specify the index of the correct option (0, 1, 2, or 3).
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
            "question": "...",
            "options": ["..", "..", "..", ".."],
            "correct_option": ""
        }}
        """)
        response_text = await self.llm_client.complete(prompt)
        response = json.loads(response_text.strip())
        return response

