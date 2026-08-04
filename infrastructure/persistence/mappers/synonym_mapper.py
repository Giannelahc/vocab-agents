
from domain.models.synonym import Synonym
from entities.synonym import SynonymModel


class SynonymMapper:

    @staticmethod
    def to_entity(model: SynonymModel) -> Synonym:

        return Synonym(
            id=model.id,
            word=model.word
        )

    @staticmethod
    def to_model(entity: Synonym) -> SynonymModel:

        return SynonymModel(
            id=entity.id,
            word=entity.word
        )

