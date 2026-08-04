
from domain.models.word_sense import WordSense
from infrastructure.persistence.entities.word_sense import WordSenseModel
from infrastructure.persistence.mappers.example_mapper import ExampleMapper
from infrastructure.persistence.mappers.synonym_mapper import SynonymMapper


class WordSenseMapper:

    @staticmethod
    def to_entity(model: WordSenseModel) -> WordSense:

        return WordSense(
            id=model.id,
            grammar_type=model.grammar_type,
            definition=model.definition,
            translations=model.translations,
            conjugation=model.conjugation,
            gender=model.gender,
            examples=[
                ExampleMapper.to_entity(e)
                for e in model.examples
            ],
            synonyms=[
                SynonymMapper.to_entity(s)
                for s in model.synonyms
            ]
        )

    @staticmethod
    def to_model(entity: WordSense) -> WordSenseModel:

        model = WordSenseModel(
            id=entity.id,
            grammar_type=entity.grammar_type,
            definition=entity.definition,
            translations=entity.translations,
            conjugation=entity.conjugation,
            gender=entity.gender
        )

        model.examples = [
            ExampleMapper.to_model(e)
            for e in entity.examples
        ]

        model.synonyms = [
            SynonymMapper.to_model(s)
            for s in entity.synonyms
        ]

        return model