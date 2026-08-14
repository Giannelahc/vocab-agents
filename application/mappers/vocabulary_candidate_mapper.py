
from domain.models.vocabulary_candidate import VocabularyCandidate
from application.enums.vocabulary_type import VocabularyType

class VocabularyCandidateMapper:

    @staticmethod
    def to_candidates(data: dict) -> list[VocabularyCandidate]:
        return [
            VocabularyCandidate(
                text=candidate["text"],
                type=VocabularyType(candidate["type"]),
                base_form=candidate["base_form"]
            )
            for candidate in data.get("candidates", [])
        ]