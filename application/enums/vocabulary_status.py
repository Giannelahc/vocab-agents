from enum import Enum


class VocabularyStatus(str, Enum):
    INVALID = "INVALID"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"