
from domain.models.vocabulary_word import VocabularyWord
from domain.models.vocabulary_word_summary import VocabularyWordSummary
from domain.models.word_sense import WordSense
from domain.models.example import Example
from domain.models.synonym import Synonym
from domain.models.user_example import UserExample
from schemas.vocabulary import (VocabularyWordResponse, 
                                WordSenseResponse, 
                                ExampleResponse,
                                UserExampleResponse,
                                SynonymResponse,
                                VocabularyListResponse,
                                VocabularyWordSummaryResponse)
from api.mappers.user_preference_mapper import LanguageMapper


class VocabularyMapper:

    @staticmethod
    def to_vocabulary_list_response(
        entity_list: list[VocabularyWordSummary],
        page: int,
        page_size: int,
        total: int
    ) -> VocabularyListResponse:
        return VocabularyListResponse(
            page= page,
            page_size= page_size,
            total= total,
            items= [
                VocabularyMapper.to_vocabulary_word_summary_response(word)
                for word in entity_list
            ],
        )

    @staticmethod
    def to_vocabulary_word_summary_response(entity: VocabularyWordSummary) -> VocabularyWordSummaryResponse:
        return VocabularyWordSummaryResponse(
            id=entity.id,
            word=entity.word,
            language=LanguageMapper.to_request(entity.language),
            status=entity.status.value,
            senses=entity.senses
        )


    @staticmethod
    def to_response(entity: VocabularyWord) -> VocabularyWordResponse:
        review_response = VocabularyWordResponse(
            id=entity.id,
            word=entity.word,
            language=LanguageMapper.to_request(entity.language),
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
            properties=entity.properties,
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