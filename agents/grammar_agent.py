import json

class GrammarAgent:
    def __init__(self, llm):
        self.llm = llm

    def get_gender(self, word, target_language):
        prompt = f"""
        '{word}' in {target_language} is masculine or feminine
        If it does not have a gender, just use 'ND'
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
          "gender": "..",
        }}
        """
        response = json.loads(self.llm(prompt))
        return response["gender"]
    
    def get_conjugation(self, word, target_language):
        prompt = f"""
        Provide the conjugation present tense used for this '{word}' in {target_language}, 
        for the first singular person and for first and third person in plural
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
          "conjugation": ["", "", ""],
        }}
        """
        response = json.loads(self.llm(prompt))
        return response["conjugation"]