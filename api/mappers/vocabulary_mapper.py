
from domain.models.vocabulary_word import VocabularyWord
from domain.models.word_sense import WordSense
from domain.models.example import Example
from domain.models.synonym import Synonym
from domain.models.user_example import UserExample
from schemas.vocabulary import (VocabularyWordResponse, 
                                WordSenseResponse, 
                                ExampleResponse,
                                UserExampleResponse,
                                SynonymResponse)


class VocabularyMapper:

    @staticmethod
    def to_list_response(entity_list: list[VocabularyWord]) -> list[VocabularyWordResponse]:
        word_list = [
                VocabularyMapper.to_response(word)
                for word in entity_list
                ]
        return word_list

    @staticmethod
    def to_response(entity: VocabularyWord) -> VocabularyWordResponse:
        review_response = VocabularyWordResponse(
            id=entity.id,
            word=entity.word,
            language_id=entity.language_id,
            status=entity.status.value,
            senses=[
                WordSenseMapper.to_response(sense) 
                for sense in entity.senses
                ]
        )
        return review_response


class WordSenseMapper:

    @staticmethod
    def to_response(entity: WordSense) -> WordSenseResponse:
        word_sense = WordSenseResponse(
            id=entity.id,
            grammar_type= entity.grammar_type,
            definition=entity.definition,
            translations=entity.translations,
            conjugation=entity.conjugation,
            gender=entity.gender,
            examples=[
                    ExampleMapper.to_response(example) 
                    for example in entity.examples
                    ],
            synonyms=[
                    SynonymMapper.to_response(synonym) 
                    for synonym in entity.synonyms
                    ],
            user_examples=[
                    UserExampleMapper.to_response(user_example) 
                    for user_example in entity.user_examples
                    ],
        )
        return word_sense

class ExampleMapper:

    @staticmethod
    def to_response(entity: Example) -> ExampleResponse:
        return ExampleResponse(
            id=entity.id,
            sentence=entity.sentence
        )

class SynonymMapper:

    @staticmethod
    def to_response(entity: Synonym) -> SynonymResponse:
        return SynonymResponse(
            id=entity.id,
            word=entity.word
        )

class UserExampleMapper:

    @staticmethod
    def to_response(entity: UserExample) -> UserExampleResponse:
        return UserExampleResponse(
            id=entity.id,
            sentence=entity.sentence
        )