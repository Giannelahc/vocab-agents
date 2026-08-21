
from domain.models.vocabulary_word import VocabularyWord
from infrastructure.persistence.entities.vocabulary_word import VocabularyWordModel
from infrastructure.persistence.enums.vocabulary_status import VocabularyStatus
from application.enums.vocabulary_status import VocabularyStatus as AppVocabularyStatus
from infrastructure.persistence.mappers.word_sense_mapper import WordSenseMapper


class VocabularyWordMapper:

    @staticmethod
    def to_entity(model: VocabularyWordModel) -> VocabularyWord:

        return VocabularyWord(
            id=model.id,
            word=model.word,
            language_id=model.language_id,
            language= model.language,
            status=AppVocabularyStatus(model.status.value),
            senses=[
                WordSenseMapper.to_entity(sense)
                for sense in model.senses
            ]
        )

    @staticmethod
    def to_model(entity: VocabularyWord) -> VocabularyWordModel:

        model = VocabularyWordModel(
            id=entity.id,
            word=entity.word,
            language_id=entity.language_id,
            status=VocabularyStatus(entity.status.value)
        )

        model.senses = [
            WordSenseMapper.to_model(sense)
            for sense in entity.senses
        ]

        return model
