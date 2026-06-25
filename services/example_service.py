import json

class ExampleService:
    def __init__(self, llm, serapi):
        self.llm = llm
        self.serapi = serapi

    def get_examples(self, word: str, tag: str, language_detected: str):
        return self.get_examples_from_serapi_search(word, tag, language_detected)
    
    def get_examples_from_serapi_search(self, word: str, tag: str, language_detected: str):
        query = f'{word} examples in {language_detected}'
        try:
            examples = self.serapi(query)
            return self.process_examples(word, tag, examples, language_detected)
        except Exception as e:
            print("SerAPI search error:", e)
        return None

    def process_examples(self, word,  tag: str, examples, language_detected):
        clean_write = f"""Clean and rewrite 3 examples the word '{word}' as '{tag}' base on these examples
                        {examples}. """
        prompt = f""" {clean_write}. Everything must be in {language_detected}, 
        filter the examples you consider most appropiates and important and all 
        of the information must be compact in examples field in the json
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
          "examples": "[.., .., ..]"
        }}
        """
        response = self.llm(prompt)
        return json.loads(response)