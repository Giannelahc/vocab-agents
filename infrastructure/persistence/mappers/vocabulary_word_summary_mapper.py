
from domain.models.vocabulary_word_summary import VocabularyWordSummary
from infrastructure.persistence.entities.vocabulary_word import VocabularyWordModel
from infrastructure.persistence.enums.vocabulary_status import VocabularyStatus
from application.enums.vocabulary_status import VocabularyStatus as AppVocabularyStatus
from infrastructure.persistence.mappers.word_sense_mapper import WordSenseMapper


class VocabularyWordSummaryMapper:

    @staticmethod
    def to_entity(model: VocabularyWordModel, count_sense: int) -> VocabularyWordSummary:

        return VocabularyWordSummary(
            id=model.id,
            word=model.word,
            language_id=model.language_id,
            language= model.language,
            status=AppVocabularyStatus(model.status.value),
            senses= count_sense
        )

