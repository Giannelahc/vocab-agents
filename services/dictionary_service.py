import json

class DictionaryService:
    def __init__(self, llm, serapi):
        self.llm = llm
        self.serapi = serapi

    def get_definition(self, word: str, target_language: str):
        return self.get_from_serapi_search(word, target_language)
    
    def get_from_serapi_search(self, word: str, target_language: str):
        query = f'"{word}" definition in {target_language}'
        try:
            definitions = self.serapi(query)
            return self.process_definitions(word, definitions, target_language)
        except Exception as e:
            print("SerAPI search error:", e)
        return None

    def process_definitions(self, word, definitions, target_language):
        prompt = f"""
        Clean and rewrite a definition for the word '{word}' base on these definitions
        {definitions}. It must be in {target_language}, 
        filter the definitions you consider most appropiates and important and all 
        of the information must be compact in definition field in the json
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
          "definition": "...",
        }}
        """
        response = self.llm(prompt)
        return json.loads(response)