from src.search_examples import search_examples
from src.agent import process_examples, get_definition, analyze_tone, get_grammar_specification
from entities.language import Language
from entities.user import User
from entities.user_learning_language import UserLearningLanguage
from entities.user_preferences import UserPreference
from agents import definition_agent
from database import SessionLocal, init_db
from configs import llm_config, serapi_config
from services import user_preference, dictionary_service

def vocabulary_agent(word):
    # 1️⃣ Guardar palabra
    with SessionLocal() as session:

        """ definition = get_definition(word, language)
        
        grammar_spec = get_grammar_specification(word)

        new_word = Word(word=word, language=language, first_definition=definition["definition_spanish"], 
                        second_definition=definition["definition_other"], 
                        first_grammar_spec = grammar_spec["spec_eng"], 
                        second_grammar_spec = grammar_spec["spec_fr"])

        session.add(new_word)
        session.commit()

        # 2️⃣ Buscar ejemplos en web
        examples = search_examples(word)

        # 3️⃣ Limpiar y analizar con IA
        cleaned_text = process_examples(word, examples)

        # 4️⃣ Guardar ejemplos en DB (simplificado)
        for line in cleaned_text.split("\n"):
            if line.strip():
                example = Example(word_id=new_word.id, 
                                  example=line.strip(), 
                                  grammar_note=analyze_tone(line.strip()))
                session.add(example)

        session.commit() """

        ##
        '''
        spanish = Language(name="Spanish", code="es")
        french = Language(name="French", code="fr")
        english = Language(name="English", code="en")

        session.add_all([spanish, french, english])
        session.commit()

        user = User(name="Giannela", lastname="Huamani", username= "giannela")
        session.add(user)
        session.commit()  # commit para tener el user.id

        # 2️⃣ Crear preferencias
        pref = UserPreference(
            user_id=user.id,
            native_language_id=spanish.id  # idioma nativo
        )

        # 3️⃣ Crear idiomas de aprendizaje
        learning1 = UserLearningLanguage(language_id=french.id)
        learning2 = UserLearningLanguage(language_id=english.id)

        # 4️⃣ Asociar al UserPreference
        pref.learning_languages.append(learning1)
        pref.learning_languages.append(learning2)

        # 5️⃣ Guardar todo
        session.add(pref)
        session.commit()'''

        user_pref = user_preference.UserPreferenceService(db_session=session)

        pref = user_pref.get_user_preferences(user_id=1)

        target_languages = [
            lang.language.name for lang in pref.learning_languages
        ]

        if pref.native_language.name not in target_languages:
            target_languages.append(pref.native_language.name)

        agent = definition_agent.DefinitionAgent(dictionary_service.DictionaryService(
            llm_config.get_llm_response, serapi_config.get_serapi_conf))
        
        result = {}

        for target in target_languages:
            result[target] = {
                "definition": agent.run(word=word, target_language=target)
            }

        print(result)
        print(f"Palabra '{word}' procesada y guardada en DB")


if __name__ == "__main__":
    init_db()
    vocabulary_agent("craindre")