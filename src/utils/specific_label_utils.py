from functools import lru_cache

import pandas as pd
import string
from spellchecker import SpellChecker

from constants import KEYBOARD_NEIGHBORS, MISSPELLING_PATTERNS, OCR_DICT, OCR_LETTER_TO_NUMBER_MAPPING, OCR_NUMBER_TO_NUMBER_MAPPING, get_misspellings_list
from error_types import ErrorType
from tokenizer import Tokenizer

MISSPELLINGS_LIST = get_misspellings_list()
tokenizer = Tokenizer()
spell = SpellChecker()

def no_labels(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset: pd.DataFrame) -> pd.Series:
    return pd.Series(0, index=data_column.index, dtype=int)

def set_all_labels_to_ocr(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset: pd.DataFrame) -> pd.Series:
    label_column = pd.Series(0, index=data_column.index, dtype=int)
    label_column.loc[generic_labeled_cell_indices] = ErrorType.OCR.value
    return label_column

def differentiate_errors_in_string_column(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset: pd.DataFrame, categorical_values: list[str] = None) -> pd.Series:
    label_column = pd.Series(0, index=data_column.index, dtype=int)
    flawed_words_series = generic_labeled_dataset.loc[generic_labeled_cell_indices]
    unique_flawed_words = flawed_words_series.unique()

    correct_words_list = categorical_values if categorical_values is not None else spell
    
    typo_word_map = {}

    for word in unique_flawed_words:
        if is_misspelling(word, correct_words_list):
            typo_word_map[word] = ErrorType.MISSPELLING.value
        elif is_transposition(word, correct_words_list):
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


#  --- Typo detection ---

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

#  --- Number labeling Typos and OCRs ---

def differentiate_errors_in_number_column(data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset: pd.DataFrame, label_func: callable = None, min_value: float = None, max_value: float = None) -> pd.Series:
    """
    This function applies a specific labeling function to differentiate errors in number columns.
    Parameters:
    - data_column: pd.Series - The column of data to be labeled.
    - generic_labeled_cell_indices: pd.Index - The indices of the cells that have been labeled in the generic dataset.
    - generic_labeled_dataset: pd.DataFrame - The dataset containing the generic labels.
    - function: callable - The function to apply for labeling. It takes as input a single word and returns the ErrorType. The label_number function (which contains a set of rules for distinguishing typos and OCRs for numbers) will never be applied in case a label_func is specified. You can call it from the label_func, if you want.
    - min_value: float - The minimum value of the number.
    - max_value: float - The maximum value of the number.
    """
    label_column = pd.Series(0, index=data_column.index, dtype=int)
    flawed_words_series = generic_labeled_dataset.loc[generic_labeled_cell_indices]
    unique_flawed_words = flawed_words_series.unique()

    typo_word_map = {}

    for word in unique_flawed_words:
        if label_func:
            typo_word_map[word] = label_func(word, min_value, max_value) 
        else:
            typo_word_map[word] = label_number_with_ocr_or_typo(word, min_value, max_value)

    # Remap results back to the original indices
    for index, word in flawed_words_series.items():
        if typo_word_map.get(word, False):
            label_column.loc[index] = typo_word_map[word]

    return label_column

def label_number_with_ocr_or_typo(word: str | int | float, min_value: float = None, max_value: float = None):
    """
    Method, which can be used to label numbers with errors, in case there is no column-specific labeling function for numbers defined.
    It distinguishes between typos and OCRs for numbers.
    """
    
    word = str(word)
    if word[-1] in [".", ",", "-"]: # we assume a number like 8743. that ends with a . is an OCR, although it could theoretically be a deletion or insertion typo
        return ErrorType.OCR.value

    if word[0] == "0" and word[1] != ".": # we assume a number like 08.1 that starts with a 0 is an OCR, although it could theoretically be a hard to detect typo of 80.1.
        return get_label_for_number_with_0_prefix(word, min_value, max_value)

    if " " in word:
        return ErrorType.OCR.value

    if has_letter_mapping_to_ocr_number(word):
        return ErrorType.OCR.value
    
    if contains_letter(word): # this covers all letters that are not OCRs (because we already checked for OCR letters), therefore we can label them as typos
        return ErrorType.TYPO.value

    if min_value is not None and max_value is not None:
        if is_replaced_ocr_in_range(word, min_value, max_value): # values like 77 would be replaced to 17, 71 or 11, which could be in range and therefore labeled as OCR instead of typo
            return ErrorType.OCR.value

    # TODO: When improveing the generic labeling of a number column, print, which values are labeled as Typos to see if they are really typos or if we can label them as OCRs.
    # print("Typo: ", word)

    # TODO: Check if it is necessary to differentiate further. We would need concrete examples of where a typo was introduced in a number column.
    return ErrorType.TYPO.value


def contains_letter(word: str) -> bool:
    """
    Check if the given word contains any letter (a-z or A-Z).
    """
    return any(char.isalpha() for char in word)


def get_label_for_number_with_0_prefix(word, min_value: float = None, max_value: float = None):
    try:
        num = float(word[1] + word[0] + word[2:]) # switch first two characters
        if (min_value is not None and min_value <= num) and (max_value is not None and num <= max_value):
            return ErrorType.TYPO.value
    except ValueError:
        return ErrorType.OCR.value
    return ErrorType.OCR.value

def has_letter_mapping_to_ocr_number(word: str | int | float):
    for char in word: # check if any letter in the word maps to a number with OCR
        if char in OCR_LETTER_TO_NUMBER_MAPPING.keys():
            return True
    return False

def is_replaced_ocr_in_range(word: str | int | float, min_value: float, max_value: float):
    """
    This function checks if a word is an OCR and whether the corrected number is within the given range.
    It replaces all occurences of the OCR with the replacement and checks if the resulting number is within the given range.
    This function assumes that there are no letters in the word.
    """
    for char in str(word):
        alternative_numbers = OCR_NUMBER_TO_NUMBER_MAPPING.get(char)
        if not alternative_numbers: # standard / forward lookup in OCR_NUMBER_TO_NUMBER_MAPPING
            continue

        for replacement_num in alternative_numbers:
            if min_value <= float(word.replace(char, replacement_num)) <= max_value: # this replaces all occurences of the char in the word
                return True

    # TODO: We only check for one OCR replacement at a time. This is usually sufficient for cases like 77 in range (0, 30), but there could be cases like 78 in range (0, 10) where we would have to replace both 7 and 8 simultaneously.
    return False


#  --- Misspelling detection ---

def is_misspelling(word, correct_words_list):
    if word in MISSPELLINGS_LIST and not word in correct_words_list:
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


#  --- More specific labeling functions ---

def label_year(token: str, min_value: float = None, max_value: float = None) -> int:
    """
    Distinguish different types of errors in a year token.
    """
    if min_value is None:
        min_value = 1880
    if max_value is None:
        max_value = 2025

    token = token.lower()
    if len(token) != 4: # cases like 20213 or 203
        return ErrorType.TYPO.value
    
    string_years = [str(i) for i in range(min_value, max_value)]
    if is_key_error(token, string_years): # case of exactly 4 numbers
        return ErrorType.TYPO.value

    return ErrorType.OCR.value # otherwise assume it's OCR

