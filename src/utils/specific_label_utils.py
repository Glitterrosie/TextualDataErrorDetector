from functools import lru_cache

import pandas as pd
import string
from spellchecker import SpellChecker

from constants import KEYBOARD_NEIGHBORS, MISSPELLING_PATTERNS
from error_types import ErrorType
from tokenizer import Tokenizer

tokenizer = Tokenizer()

spell = SpellChecker()

def no_labels(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset: pd.DataFrame) -> pd.Series:
    return pd.Series(0, index=data_column.index, dtype=int)

def set_all_labels_to_ocr(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset: pd.DataFrame) -> pd.Series:
    label_column = pd.Series(0, index=data_column.index, dtype=int)
    label_column.loc[generic_labeled_cell_indices] = ErrorType.OCR.value
    return label_column

def differentiate_errors_in_categorical_columns(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset: pd.DataFrame, categorical_values: list[str] = None) -> pd.Series:
    label_column = pd.Series(0, index=data_column.index, dtype=int)
    flawed_words_series = generic_labeled_dataset.loc[generic_labeled_cell_indices]
    unique_flawed_words = flawed_words_series.unique()

    correct_words_list = categorical_values if categorical_values is not None else spell
    
    typo_word_map = {}

    for word in unique_flawed_words:
        if is_transposition(word, correct_words_list):
            typo_word_map[word] = ErrorType.TYPO.value
        elif is_key_error(word, correct_words_list):
            typo_word_map[word] = ErrorType.TYPO.value
        elif is_deletion(word, correct_words_list):
            typo_word_map[word] = ErrorType.TYPO.value
        elif is_insertion_or_replication(word, correct_words_list):
            typo_word_map[word] = ErrorType.TYPO.value
        elif has_linguistic_misspelling_pattern(word, correct_words_list):
            typo_word_map[word] = ErrorType.MISSPELLING.value
        else:
            typo_word_map[word] = ErrorType.OCR.value


    # Remap results back to the original indices
    for index, word in flawed_words_series.items():
        if typo_word_map.get(word, False):
            label_column.loc[index] = typo_word_map[word]

    return label_column

def differentiate_errors_in_number_columns(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset: pd.DataFrame, label_func: callable) -> pd.Series:
    """
    This function applies a specific labeling function to differentiate errors in number columns.
    Parameters:
    - data_column: pd.Series - The column of data to be labeled.
    - generic_labeled_cell_indices: pd.Index - The indices of the cells that have been labeled in the generic dataset.
    - generic_labeled_dataset: pd.DataFrame - The dataset containing the generic labels.
    - function: callable - The function to apply for labeling. It takes as input a single word and returns the ErrorType.
    
    """
    label_column = pd.Series(0, index=data_column.index, dtype=int)
    flawed_words_series = generic_labeled_dataset.loc[generic_labeled_cell_indices]
    unique_flawed_words = flawed_words_series.unique()

    typo_word_map = {}

    for word in unique_flawed_words:
        typo_word_map[word] = label_func(word) 

    # Remap results back to the original indices
    for index, word in flawed_words_series.items():
        if typo_word_map.get(word, False):
            label_column.loc[index] = typo_word_map[word]

    return label_column


def is_transposition(word, correct_words_list):
    for i in range(len(word) - 1):
        chars = list(word)
        chars[i], chars[i+1] = chars[i+1], chars[i]
        candidate = ''.join(chars)
        if candidate in correct_words_list:
            return True
    return False

def is_key_error(word, correct_words_list):
    word_lower = word.lower()
    
    for i, char in enumerate(word_lower):
        neighbors = KEYBOARD_NEIGHBORS.get(char)
        if neighbors:
            word_prefix = word_lower[:i]
            word_suffix = word_lower[i+1:]
            if any(word_prefix + neighbor + word_suffix in correct_words_list for neighbor in neighbors):
                return True
    return False

def is_deletion(word, correct_words_list):
    word = word.lower()
    if correct_words_list != spell:
        correct_words_list = set(w.lower() for w in correct_words_list)
    alphabet = string.ascii_lowercase
    for i in range(len(word) + 1):
        for char in alphabet:
            candidate = word[:i] + char + word[i:]
            if candidate in correct_words_list:
                return True
    return False
    
def is_insertion_or_replication(word, correct_words_list):
    for i in range(len(word)):
        candidate = word[:i] + word[i+1:]
        if candidate in correct_words_list:
            return True
    return False    

def has_linguistic_misspelling_pattern(word, correct_words_list):
    word = word.lower()

    for pattern_type, pattern_list in MISSPELLING_PATTERNS.items():
        for wrong_seq, correct_seq in pattern_list:
            if wrong_seq in word:
                candidate = word.replace(wrong_seq, correct_seq, 1)
                if candidate in correct_words_list:
                    return pattern_type
    return None

def label_year(token: str) -> int:
    """
    Distinguish different types of errors in a year token.
    """
    token = token.lower()
    if len(token) != 4: # cases like 20213 or 203
        return ErrorType.TYPO.value
    
    string_years = [str(i) for i in range(1880, 2025)]
    if is_key_error(token, string_years): # case of exactly 4 numbers
        return ErrorType.TYPO.value

    return ErrorType.OCR.value # otherwise assume it's OCR
