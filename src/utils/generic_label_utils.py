import pandas as pd
from spellchecker import SpellChecker

from tokenizer import Tokenizer

tokenizer = Tokenizer()
spell = SpellChecker()

def empty_method(value: str):
    pass

def is_not_a_number(value: str) -> bool:
    """
    Check if a string can be converted to an integer or float.
    """
    try:
        float(value)
        return 0
    except ValueError:
        return 1

def is_a_number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def check_with_spelling_library(value: str) -> bool:
    tokenized_values = tokenizer.tokenize_cell(value)
    for token in tokenized_values:
        if spell.unknown([token]):
            return token # return the first misspelled token (early return)
    return 0

