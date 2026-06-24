import json

class DictionaryService:
    def __init__(self, llm, serapi):
        self.llm = llm
        self.serapi = serapi

    def get_definition(self, word: str, tag: str, target_languages, language_detected: str):
        return self.get_from_serapi_search(word, tag, target_languages, language_detected)
    
    def get_from_serapi_search(self, word: str, tag: str, target_languages, language_detected: str):
        query = f'{word} meaning '
        try:
            definitions = self.serapi(query)
            return self.process_definitions(word, tag, definitions, target_languages, language_detected)
        except Exception as e:
            print("SerAPI search error:", e)
        return None

    def process_definitions(self, word,  tag: str, definitions, target_languages, language_detected):
        clean_write = f"""Clean and rewrite a definition for the word '{word}' as '{tag}' base on these definitions
                        {definitions}. """
        new_definitions = f"""Write definition for the word  '{word}' as '{tag}' """
        definitions_default = new_definitions if definitions == None else clean_write
        prompt = f""" {definitions_default}. Everything must be in {language_detected}, 
        {'in synonyms field add synonyms for this {word} '
        'Add equivalents or translations of the word in those languages {target_languages}'}
        filter the definitions you consider most appropiates and important and all 
        of the information must be compact in definition field in the json
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
          "synonyms": "[.., .., ..]",
          "equivalents": "[
            "english": "[.., .., ..]",
            "portuguese": "[.., .., ..]"
          ]",
          "definition": "..."
        }}
        """
        response = self.llm(prompt)
        return json.loads(response)