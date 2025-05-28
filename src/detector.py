import re
import time
from abc import ABC, abstractmethod
from functools import lru_cache

import numpy as np
import pandas as pd
from spellchecker import SpellChecker

from constants import KEYBOARD_NEIGHBORS, MISSPELLING_PATTERNS, OCR_CHARACTER_CONFUSIONS
from error_types import ErrorType
from io_handler import IOHandler

spell = SpellChecker()


class Detector(ABC):
    def __init__(self, dataset_path: str):
        self.io_handler = IOHandler(dataset_path)
        self.dataset = self.io_handler.import_dataset()
        self.labels = pd.DataFrame(ErrorType.NO_ERROR.value, index=self.dataset.index, columns=self.dataset.columns)
        self.generic_labeled_dataset = None

    def export(self):
        self.io_handler.export_labels(self.labels)

    def detect(self):
        """
        Detects the errors in the dataset.
        """

        self.generic_labeled_dataset = pd.DataFrame(0, index=self.dataset.index, columns=self.dataset.columns)
        column_generic_label_mapping = self.get_column_generic_label_mapping()
        for column_name in self.dataset.columns:
            if column_name not in column_generic_label_mapping:
                print(f"Warning: Column '{column_name}' not found in generic label mapping. Skipping.")
                continue

            label_function = column_generic_label_mapping[column_name]
            self.generic_labeled_dataset[column_name] = self.dataset[column_name].apply(label_function)

        specific_column_label_mapping = self.get_column_specific_label_mapping()
        for column_name in self.dataset.columns:
            generic_labeled_cell_indices = self._get_generic_labeled_cell_indices(column_name)

            # each column has its own mapping function how to assign specific error types to the generic labeled cells
            label_function = specific_column_label_mapping[column_name]
            self.labels[column_name] = label_function(self.dataset[column_name], generic_labeled_cell_indices)

    @abstractmethod
    def get_column_generic_label_mapping(self) -> dict:
        pass

    @abstractmethod
    def get_column_specific_label_mapping(self) -> dict:
        pass

    def _get_generic_labeled_cell_indices(self, column_name: str) -> pd.Index:
        """
        Returns the indices of the cells that are labeled as generic.
        """
        if column_name not in self.generic_labeled_dataset.columns:
            raise ValueError(f"Column '{column_name}' not found in generic labeled dataset.")
        
        return self.generic_labeled_dataset[self.generic_labeled_dataset[column_name] == 1].index

        


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
                if col in number_columns and self.generic_labeled_dataset.loc[row, col] == 1: # we mark numbers with mistakes as OCR
                    self.labels.loc[row, col] = ErrorType.OCR.value
                    self.generic_labeled_dataset.loc[row, col] = 0 # reset to prevent double labeling
                # if any(self.word_has_ocr_character_pattern(word) for word in words):
                #         self.labels.loc[row, col] = ErrorType.OCR.value
                #         self.spellchecked_dataset.loc[row, col] = 0 # reset to prevent double labeling

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
        typo_check = self.word_has_typo_from_neighboring_keys_cached
        transposition_check = self.word_has_transposition_cached
        error_type_value = ErrorType.TYPO.value
        
        spellchecked_data = self.generic_labeled_dataset.values
        rows_to_check, cols_to_check = np.where(spellchecked_data == 1)
        total_cells = len(rows_to_check)
        
        print(f"Processing {total_cells} cells for typo detection...")
        
        start_time = time.time()
        typos_found = 0
        report_interval = max(1000, total_cells // 100)  # Report every 1% or 1000 cells
        
        for i, (row_idx, col_idx) in enumerate(zip(rows_to_check, cols_to_check)):
            words = self.tokenized_dataset.values[row_idx, col_idx]
            
            if words:
                for word in words:
                    if typo_check(word) or transposition_check(word):
                        self.labels.values[row_idx, col_idx] = error_type_value
                        self.generic_labeled_dataset.values[row_idx, col_idx] = 0
                        typos_found += 1
                        break
            
            # Print progress every N cells
            if (i + 1) % report_interval == 0:
                elapsed = time.time() - start_time
                progress = (i + 1) / total_cells * 100
                speed = (i + 1) / elapsed
                eta = (total_cells - i - 1) / speed if speed > 0 else 0
                
                print(f"Progress: {i+1:,}/{total_cells:,} ({progress:.1f}%) - "
                    f"Speed: {speed:.1f} cells/s - "
                    f"ETA: {eta:.0f}s - "
                    f"Typos found: {typos_found}")
        
        elapsed = time.time() - start_time
        print(f"Completed! Processed {total_cells:,} cells in {elapsed:.2f}s")
        print(f"Found {typos_found} typos total ({total_cells/elapsed:.1f} cells/s)")


    @lru_cache(maxsize=20000)  # Increased cache size
    def word_has_typo_from_neighboring_keys_cached(self, word):
        word_lower = word.lower()

        if word_lower in spell:
            return False
        
        # Pre-filter: only check if word contains keys that have neighbors
        if not any(char in KEYBOARD_NEIGHBORS for char in word_lower):
            return False
        
        # Use enumerate with direct neighbor lookup
        for i, char in enumerate(word_lower):
            neighbors = KEYBOARD_NEIGHBORS.get(char)
            if neighbors:
                word_prefix = word_lower[:i]
                word_suffix = word_lower[i+1:]
                # Check all neighbors at once
                if any(word_prefix + neighbor + word_suffix in spell 
                    for neighbor in neighbors):
                    return True
        return False


    @lru_cache(maxsize=20000)
    def word_has_transposition_cached(self, word):
        candidates = spell.candidates(word)
        if not candidates:
            return False
        
        word_len = len(word)
        for candidate in candidates:
            if len(candidate) == word_len and self._is_transposition_error(word, candidate):
                return True
        return False


    def _is_transposition_error(self, word, correct_word):
        # Count differences while finding positions
        diff_count = 0
        first_diff = -1
        second_diff = -1
        
        for i, (c1, c2) in enumerate(zip(word, correct_word)):
            if c1 != c2:
                diff_count += 1
                if diff_count == 1:
                    first_diff = i
                elif diff_count == 2:
                    second_diff = i
                else:
                    return False  # More than 2 differences
        
        # Must have exactly 2 differences that are adjacent
        return (diff_count == 2 and 
                second_diff == first_diff + 1 and
                word[first_diff] == correct_word[second_diff] and
                word[second_diff] == correct_word[first_diff])


    # Alternative vectorized approach for even better performance
    def check_for_typo_vectorized(self):
        """Ultra-fast vectorized version using numpy operations with progress"""
        import sys
        import time

        import numpy as np

        # Create boolean mask for cells that need checking
        needs_check = self.generic_labeled_dataset.values == 1
        
        if not np.any(needs_check):
            print("No cells need typo checking.")
            return  # Nothing to check
        
        # Get positions that need checking
        check_positions = np.argwhere(needs_check)
        total_positions = len(check_positions)
        
        print(f"Processing {total_positions:,} cells for typo detection (vectorized)...")
        
        # Batch process using numpy operations
        typo_check = self.word_has_typo_from_neighboring_keys_cached
        transposition_check = self.word_has_transposition_cached
        error_type_value = ErrorType.TYPO.value
        
        # Direct array access for speed
        labels_array = self.labels.values
        spellchecked_array = self.generic_labeled_dataset.values
        tokenized_array = self.tokenized_dataset.values
        
        start_time = time.time()
        typos_found = 0
        report_interval = max(5000, total_positions // 20)  # Report every 5% or 5000 cells
        
        for i, (row_idx, col_idx) in enumerate(check_positions):
            words = tokenized_array[row_idx, col_idx]
            
            if words and any(typo_check(word) or transposition_check(word) for word in words):
                labels_array[row_idx, col_idx] = error_type_value
                spellchecked_array[row_idx, col_idx] = 0
                typos_found += 1
            
            # Print progress every N positions
            if (i + 1) % report_interval == 0:
                elapsed = time.time() - start_time
                progress = (i + 1) / total_positions * 100
                speed = (i + 1) / elapsed if elapsed > 0 else 0
                eta = (total_positions - i - 1) / speed if speed > 0 else 0
                
                print(f"[{progress:5.1f}%] {i+1:,}/{total_positions:,} cells | "
                    f"{speed:.1f} cells/s | ETA: {eta:.0f}s | Typos: {typos_found}")
                sys.stdout.flush()
        
        elapsed = time.time() - start_time
        print(f"Vectorized processing completed!")
        print(f"Processed {total_positions:,} cells in {elapsed:.2f}s ({total_positions/elapsed:.1f} cells/s)")
        print(f"Found {typos_found} typos total")
        sys.stdout.flush()


    def check_for_misspellings_short(self):
        for row in self.tokenized_dataset.index:
            for col in self.tokenized_dataset.columns:
                if self.generic_labeled_dataset.loc[row, col] == 1: # we mark numbers with mistakes as OCR
                    self.labels.loc[row, col] = ErrorType.MISSPELLING.value
                    self.generic_labeled_dataset.loc[row, col] = 0

############################################# Misspellings

    @lru_cache(maxsize=10000)
    def word_has_linguistic_misspelling_pattern(self, word):
        """Optimized version of the original function"""
        candidates = spell.candidates(word)
        if not candidates:
            return False
        
        for candidate in candidates:
            if self.has_linguistic_misspelling_pattern(word, candidate):
                return True
        return False
    
    def has_linguistic_misspelling_pattern(self, wrong_word, correct_word):
        """Optimized version of the original function"""
        for pattern_type, patterns in MISSPELLING_PATTERNS.items():
            for wrong_seq, correct_seq in patterns:
                if wrong_seq in wrong_word and correct_seq in correct_word:
                    return pattern_type
        return None

    # Alternative approach using numpy operations for even better performance
    def check_for_misspellings(self):
        """Ultra-optimized version using numpy operations"""
        print("Starting numpy-optimized misspelling check...")
        start_time = time.time()
        
        # Convert to numpy for faster operations
        spellcheck_array = self.generic_labeled_dataset.values
        tokenized_array = self.tokenized_dataset.values
        labels_array = self.labels.values
        
        # Find all positions where spellcheck == 1
        check_positions = np.where(spellcheck_array == 1)
        total_positions = len(check_positions[0])
        
        if total_positions == 0:
            print("No positions to check.")
            return
        
        print(f"Checking {total_positions} positions...")
        
        # Process in chunks for memory efficiency
        chunk_size = 5000
        processed = 0
        
        for start_idx in range(0, total_positions, chunk_size):
            end_idx = min(start_idx + chunk_size, total_positions)
            
            # Extract chunk positions
            chunk_rows = check_positions[0][start_idx:end_idx]
            chunk_cols = check_positions[1][start_idx:end_idx]
            
            # Process chunk
            misspelling_mask = np.zeros(len(chunk_rows), dtype=bool)
            
            for i, (row, col) in enumerate(zip(chunk_rows, chunk_cols)):
                words = tokenized_array[row, col]
                if words and any(self.word_has_linguistic_misspelling_pattern(word) for word in words):
                    misspelling_mask[i] = True
            
            # Update arrays where misspellings found
            if np.any(misspelling_mask):
                update_rows = chunk_rows[misspelling_mask]
                update_cols = chunk_cols[misspelling_mask]
                
                labels_array[update_rows, update_cols] = ErrorType.MISSPELLING.value
                spellcheck_array[update_rows, update_cols] = 0
            
            processed = end_idx
            progress = (processed / total_positions) * 100
            elapsed = time.time() - start_time
            eta = (elapsed / processed) * (total_positions - processed) if processed > 0 else 0
            
            print(f"Progress: {processed}/{total_positions} ({progress:.1f}%) - "
                f"Elapsed: {elapsed:.1f}s - ETA: {eta:.1f}s")
        
        # Update original dataframes
        self.labels.iloc[:, :] = labels_array
        self.generic_labeled_dataset.iloc[:, :] = spellcheck_array
        
        total_time = time.time() - start_time
        print(f"Numpy-optimized misspelling check completed in {total_time:.2f} seconds")


    def _tokenize(self):
        tokenized_dataset = pd.DataFrame(list(), index=self.dataset.index, columns=self.dataset.columns)
        for column in self.dataset.columns:
            tokenized_dataset[column] = self.dataset[column].apply(
                lambda cell: [word for word in re.split(r'\W', cell) if word] # remove empty strings
            )
        return tokenized_dataset

