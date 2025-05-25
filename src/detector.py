import re
from constants import KEYBOARD_NEIGHBORS, MISSPELLING_PATTERNS, OCR_CHARACTER_CONFUSIONS
from abc import ABC, abstractmethod

import pandas as pd
from error_types import ErrorType
from io_handler import IOHandler
from spellchecker import SpellChecker

spell = SpellChecker()


class Detector(ABC):
    def __init__(self, dataset_path: str):
        self.io_handler = IOHandler(dataset_path)
        self.dataset = self.io_handler.import_dataset()
        self.labels = pd.DataFrame(ErrorType.NO_ERROR.value, index=self.dataset.index, columns=self.dataset.columns)
        self.spellchecked_dataset = None


    def detect(self, use_tokenized_dataset: bool = False):
        """
        Detects the errors in the dataset.
        This method should be implemented by subclasses.
        Parameters:
            :use_tokenized_dataset: If True, uses an already tokenized dataset for detection and skips the tokenization step.
        """
        if use_tokenized_dataset:
            self.tokenized_dataset = self.io_handler.load_pickled_dataset()
        else:
            print("Tokenizing dataset...")
            self.tokenized_dataset = self._tokenize()
            self.io_handler.save_pickled_dataset(self.tokenized_dataset)
        self.spellchecked_dataset = self.check_for_spelling_mistakes()

        print(self.tokenized_dataset.head())
        
    def export(self):
        self.io_handler.export_labels(self.labels)

    def check_for_spelling_mistakes(self): # this is a generic method using a library to find possible candidates
        result_df = pd.DataFrame(index=self.tokenized_dataset.index, columns=self.tokenized_dataset.columns)

        for row in self.tokenized_dataset.index:
            for col in self.tokenized_dataset.columns:
                words = self.tokenized_dataset.loc[row, col]
                misspelled = spell.unknown(words)
                result_df.loc[row, col] = 1 if misspelled else 0

        return result_df

        
    def check_for_ocr(self, number_columns: list[str]):
        for row in self.tokenized_dataset.index:
            for col in self.tokenized_dataset.columns:
                words = self.tokenized_dataset.loc[row, col]
                if col in number_columns and self.spellchecked_dataset.loc[row, col] == 1: # we mark numbers with mistakes as OCR
                    self.labels.loc[row, col] = ErrorType.OCR.value
                    self.spellchecked_dataset.loc[row, col] = 0 # reset to prevent double labeling
                if any(self.word_has_ocr_character_pattern(word) for word in words):
                        self.labels.loc[row, col] = ErrorType.OCR.value
                        self.spellchecked_dataset.loc[row, col] = 0 # reset to prevent double labeling

    def word_has_ocr_character_pattern(self, word):
        candidates = spell.candidates(word)
        if not candidates:
            return
        for candidate in candidates:
            if self.has_ocr_character_pattern(word, candidate):
                return True
        return False

    def has_ocr_character_pattern(self, wrong_word, correct_word):
        for wrong_char, correct_char in zip(wrong_word, correct_word):
            if wrong_char != correct_char:
                if OCR_CHARACTER_CONFUSIONS.get(wrong_char) == correct_char:
                    return True
        return False

    def check_for_typo(self):
        for row in self.tokenized_dataset.index:
            for col in self.tokenized_dataset.columns:
                if self.spellchecked_dataset.loc[row, col] == 1:
                    words = self.tokenized_dataset.loc[row, col]
                    if any(self.word_has_typo_from_neighboring_keys(word) for word in words):
                        self.labels.loc[row, col] = ErrorType.TYPO.value
                        self.spellchecked_dataset.loc[row, col] = 0 # reset to prevent double labeling
                    if any(self.word_has_transposition(word) for word in words):
                        self.labels.loc[row, col] = ErrorType.TYPO.value
                        self.spellchecked_dataset.loc[row, col] = 0 # reset to prevent double labeling


    def word_has_typo_from_neighboring_keys(self, word):
        word = word.lower()
        if word in spell:
            return False
        
        # single-character replacements using neighboring keys
        for i, char in enumerate(word):
            if char in KEYBOARD_NEIGHBORS:
                for neighbor in KEYBOARD_NEIGHBORS[char]:
                    modified = word[:i] + neighbor + word[i+1:]
                    if modified in spell:
                        return True  # Typo found
        return False

    def word_has_transposition(self, word):
        candidates = spell.candidates(word)
        if not candidates:
            return
        for candidate in candidates:
            if self.is_transposition_error(word, candidate):
                print("Found transposition error!!!")
                return True
        return False
    
    def is_transposition_error(self, word, correct_word):
        # Find positions where characters differ
        diff_positions = []
        for i, (c1, c2) in enumerate(zip(word, correct_word)):
            if c1 != c2:
                diff_positions.append(i)
        
        # For transposition, exactly 2 positions should differ and be adjacent
        if len(diff_positions) != 2:
            return False
        
        pos1, pos2 = diff_positions
        if pos2 - pos1 != 1:  # Must be adjacent so that swapping makes sense
            return False
        
        return (word[pos1] == correct_word[pos2] and word[pos2] == correct_word[pos1])
    
    def check_for_misspellings(self):
        for row in self.tokenized_dataset.index:
            for col in self.tokenized_dataset.columns:
                if self.spellchecked_dataset.loc[row, col] == 1:
                    words = self.tokenized_dataset.loc[row, col]
                    if any(self.word_has_linguistic_misspelling_pattern(word) for word in words):
                        self.labels.loc[row, col] = ErrorType.MISSPELLING.value
                        self.spellchecked_dataset.loc[row, col] = 0 # reset to prevent double labeling

    
    def word_has_linguistic_misspelling_pattern(self, word):
        candidates = spell.candidates(word)
        if not candidates:
            return
        
        for candidate in candidates:
            if self.has_linguistic_misspelling_pattern(word, candidate):
                return True

        return False
    

    def has_linguistic_misspelling_pattern(self, wrong_word, correct_word):
        for pattern_type, patterns in MISSPELLING_PATTERNS.items():
            for wrong_seq, correct_seq in patterns:
                if wrong_seq in wrong_word and correct_seq in correct_word:
                    return pattern_type
        return None


    def _tokenize(self):
        tokenized_dataset = pd.DataFrame(list(), index=self.dataset.index, columns=self.dataset.columns)
        for column in self.dataset.columns:
            tokenized_dataset[column] = self.dataset[column].apply(
                lambda cell: [word for word in re.split(r'\W', cell) if word] # remove empty strings
            )
        return tokenized_dataset

