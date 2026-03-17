from services.user_preference import UserPreferenceService

class DefinitionAgent:
    def __init__(self, llm_client, user_pref_service: UserPreferenceService):
        self.llm = llm_client
        self.user_pref_service = user_pref_service

    def run(self, word, user_id):
        source_language = self.detect_language(word)
        user_prefs = self.user_pref_service.get_user_preferences(user_id)
        target_languages = self.decide_target_languages(source_language, user_prefs)
        definitions = self.generate_definitions(word, source_language, target_languages)
        return {
            "word": word,
            "source_language": source_language,
            "definitions": definitions
        }
    
    def detect_language(self, word: str) -> str:
        prompt = f"Detect the language of this word: '{word}'. Respond only with 'english', 'spanish', or 'french'."
        return self.llm(prompt).strip().lower()

    def get_user_preferences(self, user_id: int):
        pref = self.user_pref_service.get_user_preferences(user_id=user_id)
        return pref

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

    def generate_definitions(self, word: str, source_language: str, target_languages: list) -> dict:
        targets_str = ", ".join(target_languages)
        prompt = f"""
        Provide a short dictionary definition for the word '{word}' in {source_language}.
        Give definitions in: {targets_str}.
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
          "spanish": "...",
          "english": "..."
        }}
        """
        import json
        response = self.llm(prompt)
        return json.loads(response)