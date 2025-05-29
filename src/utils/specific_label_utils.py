import pandas as pd
from error_types import ErrorType
from spellchecker import SpellChecker
from constants import KEYBOARD_NEIGHBORS, MISSPELLING_PATTERNS
from tokenizer import Tokenizer
from functools import lru_cache

tokenizer = Tokenizer()

spell = SpellChecker()

def no_labels(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset) -> pd.Series:
    return pd.Series(0, index=data_column.index, dtype=int)

def set_all_labels_to_ocr(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset) -> pd.Series:
    label_column = pd.Series(0, index=data_column.index, dtype=int)
    label_column.loc[generic_labeled_cell_indices] = ErrorType.OCR.value
    return label_column

def differentiate_errors_in_categorical_columns(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset) -> pd.Series:
    label_column = pd.Series(0, index=data_column.index, dtype=int)
    flawed_words_series = generic_labeled_dataset.loc[generic_labeled_cell_indices]
    unique_flawed_words = flawed_words_series.unique()
    
    typo_word_map = {}

    for word in unique_flawed_words:
        if is_transposition(word):
            typo_word_map[word] = ErrorType.TYPO.value
        elif is_key_error(word):
            typo_word_map[word] = ErrorType.TYPO.value
        elif has_linguistic_misspelling_pattern(word):
            typo_word_map[word] = ErrorType.MISSPELLING.value
        else:
            typo_word_map[word] = ErrorType.OCR.value


    # Remap results back to the original indices
    for index, word in flawed_words_series.items():
        if typo_word_map.get(word, False):
            label_column.loc[index] = typo_word_map[word]

    return label_column

def is_transposition(word):
    for i in range(len(word) - 1):
        chars = list(word)
        chars[i], chars[i+1] = chars[i+1], chars[i]
        candidate = ''.join(chars)
        if candidate in spell:
            return True
    return False

def is_key_error(word):
    word_lower = word.lower()
    
    for i, char in enumerate(word_lower):
        neighbors = KEYBOARD_NEIGHBORS.get(char)
        if neighbors:
            word_prefix = word_lower[:i]
            word_suffix = word_lower[i+1:]
            if any(word_prefix + neighbor + word_suffix in spell for neighbor in neighbors):
                return True
    return False
    

def has_linguistic_misspelling_pattern(word):
    word = word.lower()

    for pattern_type, pattern_list in MISSPELLING_PATTERNS.items():
        for wrong_seq, correct_seq in pattern_list:
            if wrong_seq in word:
                candidate = word.replace(wrong_seq, correct_seq, 1)
                if candidate in spell:
                    return pattern_type
    return None