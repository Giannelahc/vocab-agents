from services.dictionary_service import DictionaryService

class DefinitionAgent:
    def __init__(self, dictionary_service: DictionaryService):
        self.dictionary_service = dictionary_service

    def run(self, word, target_language):
        #source_language = self.detect_language(word)
        definitions = self.generate_definitions(word, target_language)
        return {
            "word": word,
            #"source_language": source_language,
            "definitions": definitions["definition"]
        }
    
    '''def detect_language(self, word: str) -> str:
        prompt = f"Detect the language of this word: '{word}'. Respond only with 'english', 'spanish', or 'french'."
        return self.llm(prompt).strip().lower()'''

    def decide_target_languages(self, source_language: str, user_prefs) -> list:
        targets = []

        # idioma nativo
        if user_prefs.native_language.name != source_language:
            targets.append(user_prefs.native_language.name)

        # idiomas de aprendizaje
        for ul in user_prefs.learning_languages:
            if ul.language.name != source_language:
                targets.append(ul.language.name)

        return list(set(targets))

    def generate_definitions(self, word: str, target_language: str) -> dict:
        return self.dictionary_service.get_definition(word, target_language)