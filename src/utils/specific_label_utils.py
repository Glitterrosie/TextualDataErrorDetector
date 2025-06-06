from functools import lru_cache

import pandas as pd
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

def differentiate_errors_in_categorical_columns(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset: pd.DataFrame, categorical_values_list: list[str] = None) -> pd.Series:
    label_column = pd.Series(0, index=data_column.index, dtype=int)
    flawed_words_series = generic_labeled_dataset.loc[generic_labeled_cell_indices]
    unique_flawed_words = flawed_words_series.unique()

    correct_words_list = categorical_values_list if categorical_values_list is not None else spell
    
    typo_word_map = {}

    for word in unique_flawed_words:
        if is_transposition(word, correct_words_list):
            typo_word_map[word] = ErrorType.TYPO.value
        elif is_key_error(word, correct_words_list):
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
    

def has_linguistic_misspelling_pattern(word, correct_words_list):
    word = word.lower()

    for pattern_type, pattern_list in MISSPELLING_PATTERNS.items():
        for wrong_seq, correct_seq in pattern_list:
            if wrong_seq in word:
                candidate = word.replace(wrong_seq, correct_seq, 1)
                if candidate in correct_words_list:
                    return pattern_type
    return None
