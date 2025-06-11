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
    if not is_a_number(value):
        return value
    return 0

def is_not_a_number_in_range(value: str, min_value: float, max_value: float) -> bool:
    if not is_a_number(value):
        return value
    if float(value) < min_value or float(value) > max_value:
        return value
    return 0

def is_a_number(value: str) -> bool:
    """
    Do not use this function in generic labeling, because it returns False or True, instead of 0 or the value itself.
    """
    if (value[-1] == "."): # numbers like 8743. are likely OCRs but would be converted to 8743 by the float conversion
        return False

    if (len(value) > 1 and value[0] == "0" and value[1] != "."): # numbers like 08.1 are also likely a mistake
        return False

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

