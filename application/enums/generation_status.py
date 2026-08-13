from enum import Enum


class GenerationStatus(str, Enum):
    TO_GENERATE = "TO_GENERATE"
    GENERATING = "GENERATING"
    READY = "READY"
    FAILED = "FAILED"