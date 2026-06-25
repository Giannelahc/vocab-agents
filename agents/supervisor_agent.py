from services import pos_tagger, user_preference
from agents import definition_agent, grammar_agent, example_agent

class SupervisorAgent:
    def __init__(self, user_preference_service: user_preference.UserPreferenceService, 
                 pos_tagger: pos_tagger.PosTaggerService, 
                 definition_agent: definition_agent.DefinitionAgent,
                 grammar_agent: grammar_agent.GrammarAgent,
                 example_agent: example_agent.ExampleAgent):
        self.preference_service = user_preference_service
        self.pos_tagger_service = pos_tagger
        self.definition_agent = definition_agent
        self.grammar_agent = grammar_agent
        self.example_agent = example_agent

    def run(self, word, user_id, language_detected):
        target_languages = self.get_target_languages(user_id)
        result = {}

        types = self.pos_tagger_service.process_word(word, language_detected)["types"]
        result[language_detected] = {}
        for type in types:
            print(type)
            tasks = self.decide_tasks(type)
            print(tasks)
            result[language_detected] = self.execute_tasks(tasks=tasks, word=word, tag=type, target_languages=target_languages, 
                                                           result=result[language_detected], language_detected=language_detected)

        return result


    def execute_tasks(self, tasks, word, tag, target_languages, result, language_detected):
        print(language_detected)
        result[tag] = self.definition_agent.run(word=word, tag=tag, target_languages=target_languages, language_detected = language_detected)
        if "gender_info" in tasks:
            result[tag]["gender"] = self.grammar_agent.get_gender(word, language_detected)
        if "conjugation" in tasks:
            result[tag]["conjugation"] = self.grammar_agent.get_conjugation(word, language_detected)
        if "examples" in tasks:
            result[tag]["examples"] = self.example_agent.run(word, tag, language_detected)
        
        return result


    def get_target_languages(self, user_id):
        pref = self.preference_service.get_user_preferences(user_id)

        target_languages = [
            lang.language.name for lang in pref.learning_languages
        ]
        
        if pref.native_language.name not in target_languages:
            target_languages.append(pref.native_language.name)
        return target_languages


    def decide_tasks(self, type: str):
        tasks = ["definition", "examples"]
        if type.__contains__("verb"):
            tasks.append("grammar_rules")
            tasks.append("conjugation")
        
        if type.__contains__("noun"):
            tasks.append("gender_info")

        return tasks
