import re
from functools import partial

import pandas as pd

from detector import Detector
from error_types import ErrorType
from utils.generic_label_utils import (
    check_with_spelling_library,
    empty_method,
    is_not_a_number,
)
from utils.specific_label_utils import (
    differentiate_errors_in_categorical_columns,
    differentiate_errors_in_number_columns,
    label_year,
    no_labels,
    set_all_labels_to_ocr,
)


class IMDBDetector(Detector):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)

    def detect(self):
        print(f"--- IMDB Dataset ---")
        print(f"Number of cells: {self.dataset.size}, Number of rows: {self.dataset.shape[0]}")

        super().detect() 

    def get_column_generic_label_mapping(self) -> dict:
        return {
            "cast_id": is_not_a_number,
            "cast_person_id": is_not_a_number,
            "cast_movie_id": is_not_a_number,
            "cast_person_role_id": check_with_spelling_library,
            "cast_note": check_with_spelling_library,
            "cast_nr_order": is_not_a_number,
            "cast_role_id": is_not_a_number,
            "person_id": is_not_a_number,
            "person_movie_id": check_with_spelling_library,
            "person_info_type_id": is_not_a_number,
            "extra_info": check_with_spelling_library,
            "person_note": check_with_spelling_library,
            "title_id": is_not_a_number,
            "title": check_with_spelling_library,
            "imdb_index": self._is_valid_roman_numeral,
            "kind_id": is_not_a_number,
            "production_year": self.is_not_a_production_year,
            "phonetic_code": self._is_valid_phonetic_code,
            "episode_of_id": is_not_a_number,
            "season_nr": is_not_a_number,
            "episode_nr": is_not_a_number,
            "series_years": self.is_not_a_series_years,
            "md5sum": empty_method, # TODO: check how to handle this column
            "name": check_with_spelling_library,
        }


    def get_column_specific_label_mapping(self) -> dict:
        return {
            "cast_id": set_all_labels_to_ocr,
            "cast_person_id": set_all_labels_to_ocr,
            "cast_movie_id": set_all_labels_to_ocr,
            "cast_person_role_id": differentiate_errors_in_categorical_columns,
            "cast_note": differentiate_errors_in_categorical_columns,
            "cast_nr_order": set_all_labels_to_ocr,
            "cast_role_id": set_all_labels_to_ocr,
            "person_id": set_all_labels_to_ocr,
            "person_movie_id": differentiate_errors_in_categorical_columns,
            "person_info_type_id": set_all_labels_to_ocr,
            "extra_info": differentiate_errors_in_categorical_columns,
            "person_note": differentiate_errors_in_categorical_columns,
            "title_id": set_all_labels_to_ocr,
            "title": differentiate_errors_in_categorical_columns,
            "imdb_index": set_all_labels_to_ocr,
            "kind_id": set_all_labels_to_ocr,
            "production_year": set_all_labels_to_ocr, # although we could check for valid years, we found that all wrong values in this colun are actually OCRs
            "phonetic_code": self._label_phonetic_code,
            "episode_of_id": set_all_labels_to_ocr,
            "season_nr": set_all_labels_to_ocr,
            "episode_nr": set_all_labels_to_ocr,
            "series_years": partial(differentiate_errors_in_number_columns, label_func=label_year),
            "md5sum": no_labels,
            "name": set_all_labels_to_ocr, # we checked manually, all unique values in this column are due to OCR errors
        }

    def _is_valid_phonetic_code(self, cell: str) -> int:
        """
        Returns 0 if the cell contains a valid phonetic code, else 1.
        A valid phonetic code must be a single string starting with a capital letter,
        followed by 1 to 4 digits. No spaces or multiple words allowed.
        """
        if re.fullmatch(r'[A-Z]\d{1,4}', cell):
            return 0
        return 1

    def _is_valid_roman_numeral(self, cell: str) -> int:
        """
        Returns 0 if the cell is a valid Roman numeral, else 1.
        Valid Roman numerals include I, II, III, IV, V, VI, VII, VIII, IX, X, etc.
        This regex checks up to 3999 (MMMCMXCIX).
        """
        if re.fullmatch(r'M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})', cell):
            return 0
        return 1

    def is_not_a_series_years(self, value: str) -> bool:
        """
        Check if a string is not a year (4-digit number).
        """
        tokens = self.tokenizer.tokenize_cell(value)
        for token in tokens:
            if not token.isdigit() or len(token) != 4:
                return token
        return 0

    def is_not_a_production_year(self, value: str) -> bool:
        """
        Check if a string is not a production year (4-digit number).
        """
        tokens = self.tokenizer.tokenize_cell(value)
        if not tokens[0].isdigit() or len(tokens[0]) != 4:
            return tokens[0]
        if not tokens[1].isdigit():
            return tokens[1]
        return 0

    def _label_phonetic_code(self, data_column: pd.Series, generic_labeled_cell_indices: pd.Index, generic_labeled_dataset) -> pd.Series:
        label_column = pd.Series(0, index=data_column.index, dtype=int)
        flawed_words_series = generic_labeled_dataset.loc[generic_labeled_cell_indices]
        unique_flawed_words = flawed_words_series.unique()

        error_word_map = {}
        for word in unique_flawed_words:
            if len(str(word)) > 5:
                error_word_map[word] = ErrorType.TYPO.value
            elif not str(word)[0].isupper():
                error_word_map[word] = ErrorType.TYPO.value
            else:
                error_word_map[word] = ErrorType.OCR.value

        # Remap results back to the original indices
        for index, word in flawed_words_series.items():
            if error_word_map.get(word, False):
                label_column.loc[index] = error_word_map[word]

        return label_column
