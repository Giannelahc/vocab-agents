from dataclasses import dataclass

@dataclass
class VocabularyCandidate:

    text: str
    type: str
    base_form: str
    already_registered: bool = False