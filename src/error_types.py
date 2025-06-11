
from enum import Enum


class ErrorType(Enum):
    NO_ERROR = 0
    MISSPELLING = 1
    TYPO = 2
    OCR = 3
    WORD_TRANSPOSITION = 4
