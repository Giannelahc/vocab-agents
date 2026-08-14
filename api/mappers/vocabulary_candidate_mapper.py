
from domain.models.vocabulary_candidate import VocabularyCandidate
from schemas.vocabulary import VocabularyCandidateResponse

class VocabularyCandidateMapper:

    @staticmethod
    def to_response(
        candidate: VocabularyCandidate
    ) -> VocabularyCandidateResponse:

        return VocabularyCandidateResponse(
            text=candidate.text,
            type=candidate.type,
            base_form=candidate.base_form,
            already_registered=candidate.already_registered
        )