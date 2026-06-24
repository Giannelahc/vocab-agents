import json

class PosTaggerService:
    def __init__(self, llm):
        self.llm = llm

    def getTag(self, word):
        return self.process_word(word)

    def process_word(self, word, languaje_detected):
        prompt = f"""
        Provide the grammar types 
        for example verb, noun, relative pronoun, preposition, adverb, expression and so on 
        for this '{languaje_detected}' '{word}'
        Rules:
        - Only include grammatical types that are truly used in real language.
        - If unsure, return only the most common type.
        - Do not invent meanings.
        All the types in english. Be specific to not lose information
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
          "types": ["verb", "noun"]
        }}
        """
        response = self.llm(prompt)
        return json.loads(response)