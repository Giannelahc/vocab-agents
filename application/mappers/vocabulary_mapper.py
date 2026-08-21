
from domain.models.vocabulary_word import VocabularyWord
from domain.models.vocabulary_word_summary import VocabularyWordSummary
from domain.models.word_sense import WordSense
from domain.models.example import Example
from domain.models.synonym import Synonym

class VocabularyMapper:

    def from_analysis(
        self,
        senses_data: list
    ) -> list[WordSense]:
        senses: list[WordSense] = []

        for sense_data in senses_data:

            sense = self.to_word_sense(sense_data)

            senses.append(sense)

        return senses


    def to_word_sense(self, data: dict) -> WordSense:

        sense = WordSense(
            grammar_type=data["part_of_speech"],
            definition=data["definition"],
            conjugation=data.get("conjugation"),
            properties=data.get("properties"),
            translations=data.get("translation"),
            gender=data.get("gender")
        )


        for example_sentence in data.get("examples", []):

            example = Example(
                sentence=example_sentence
            )

            sense.examples.append(example)


        for synonym_word in data.get("synonyms", []):

            synonym = Synonym(
                word=synonym_word
            )

            sense.synonyms.append(synonym)


        return sense

    def to_word_summary(word: VocabularyWord) -> VocabularyWordSummary:
        return VocabularyWordSummary(
            id=word.id,
            word=word.word,
            language_id=word.language_id,
            status=word.status
        )