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
    
def check_with_spelling_library(value: str) -> bool:
    tokenized_value = tokenizer.tokenize_cell(value)
    misspelled = spell.unknown(tokenized_value)
    return list(misspelled)[0] if misspelled else 0


