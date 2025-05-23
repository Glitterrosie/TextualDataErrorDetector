
from enum import Enum


class ErrorType(Enum):
    NO_ERROR = 0
    TYPO = 1
    MISSPELLING = 2
    OCR = 3
    WORD_TRANSPOSITION = 4
