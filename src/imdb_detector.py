import re
from functools import partial

import pandas as pd

from detector import Detector
from error_types import ErrorType
from utils.generic_label_utils import (
    check_with_spelling_library,
    is_not_a_number,
    is_a_number,
)
from utils.specific_label_utils import (
    differentiate_errors_in_string_column,
    differentiate_errors_in_number_column,
    label_year,
    set_all_labels_to_ocr,
)


class IMDBDetector(Detector):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)

    def detect(self):
        print(f"--- IMDB Dataset ---")
        print(f"Number of cells: {self.dataset.size}, Number of rows: {self.dataset.shape[0]}")

        super().detect() 
        self._label_cast_note_person_note_transpositions()
        self._label_cast_id_cast_person_id_transpositions()
        self._label_identical_columns()

    def get_column_generic_label_mapping(self) -> dict:
        return {
            "cast_id": is_not_a_number,
            "cast_person_id": is_not_a_number,
            "cast_movie_id": is_not_a_number,
            "cast_person_role_id": self.is_not_a_cast_person_role_id,
            "cast_note": check_with_spelling_library,
            "cast_nr_order": is_not_a_number,
            "cast_role_id": is_not_a_number,
            "person_id": is_not_a_number,
            "person_movie_id": is_not_a_number,
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
            "md5sum": self._is_not_a_valid_hash,
            "name": check_with_spelling_library,
        }


    def get_column_specific_label_mapping(self) -> dict:
        series_years_label_func = partial(differentiate_errors_in_number_column, label_func=label_year)
        return {
            "cast_id": set_all_labels_to_ocr,                       # IDs have no typos -> OCR
            "cast_person_id": set_all_labels_to_ocr,                # IDs have no typos -> OCR
            "cast_movie_id": set_all_labels_to_ocr,                 # IDs have no typos -> OCR
            "cast_person_role_id": set_all_labels_to_ocr,           # Manual check -> all OCRs
            "cast_note": differentiate_errors_in_string_column,
            "cast_nr_order": set_all_labels_to_ocr,                 # Manual check -> all OCRs
            "cast_role_id": set_all_labels_to_ocr,                  # IDs have no typos -> OCR
            "person_id": set_all_labels_to_ocr,                     # IDs have no typos -> OCR
            "person_movie_id": set_all_labels_to_ocr,               # IDs have no typos -> OCR
            "person_info_type_id": set_all_labels_to_ocr,           # IDs have no typos -> OCR
            "extra_info": differentiate_errors_in_string_column,
            "person_note": differentiate_errors_in_string_column,
            "title_id": set_all_labels_to_ocr,                      # IDs have no typos -> OCR
            "title": differentiate_errors_in_string_column,
            "imdb_index": set_all_labels_to_ocr,                    # Manual check -> all OCRs
            "kind_id": set_all_labels_to_ocr,                       # IDs have no typos -> OCR
            "production_year": set_all_labels_to_ocr,               # Manual check -> all OCRs
            "phonetic_code": self._label_phonetic_code,
            "episode_of_id": set_all_labels_to_ocr,                 # IDs have no typos -> OCR
            "season_nr": set_all_labels_to_ocr,                     # TODO
            "episode_nr": set_all_labels_to_ocr,                    # TODO
            "series_years": series_years_label_func,
            "md5sum": set_all_labels_to_ocr,                        # this column only contains OCRs
            "name": set_all_labels_to_ocr,                          # Manual check -> all OCRs
        }
    
    def _label_identical_columns(self):
        all_numeric = self.dataset[self.dataset['title_id'].apply(is_a_number) & self.dataset['person_movie_id'].apply(is_a_number) & self.dataset['cast_movie_id'].apply(is_a_number)]
        title_cast_match = all_numeric[(all_numeric['title_id'] != all_numeric['person_movie_id']) & (all_numeric['title_id'] == all_numeric['cast_movie_id'])] # person bad
        title_person_match = all_numeric[(all_numeric['title_id'] != all_numeric['cast_movie_id']) & (all_numeric['title_id'] == all_numeric['person_movie_id'])] # cast bad
        cast_person_match = all_numeric[(all_numeric['title_id'] != all_numeric['cast_movie_id']) & (all_numeric['cast_movie_id'] == all_numeric['person_movie_id'])] # title bad

        self.labels.loc[title_cast_match.index, 'person_movie_id'] = ErrorType.OCR.value
        self.labels.loc[title_person_match.index, 'cast_movie_id'] = ErrorType.OCR.value
        self.labels.loc[cast_person_match.index, 'title_id'] = ErrorType.OCR.value

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
        Check if a string is not a production year (4-digit number) in format YYYY.0.
        """
        tokens = self.tokenizer.tokenize_cell(value)
        if not tokens[0].isdigit() or len(tokens[0]) != 4:
            return tokens[0]
        if not tokens[1].isdigit():
            return tokens[1]
        return 0
    
    def is_not_a_cast_person_role_id(self, value):
        try:
            value = float(value)
            if value != 999999.0:
                return 1
            return 0
        except ValueError:
            return 1

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
    
    def _is_not_a_valid_hash(self, value: str):
        return all(c in "0123456789abcdefABCDEF" for c in value)

    def _label_cast_note_person_note_transpositions(self):
        """
        The cast_note and person_note columns have transpositions. The rule we found (which does not hold in all cases) is that
        the cast_note is round braces, while the person_note is only sometimes in braces.
        """
        person_note_in_braces = self.dataset[self.dataset['person_note'].str.startswith('(') & self.dataset['person_note'].str.endswith(')')]
        self._label_word_transpositions(column_names=["cast_note", "person_note"], row_indices=person_note_in_braces.index)
 
    def _label_cast_id_cast_person_id_transpositions(self):
        """
        The cast_id and cast_person_id columns have transpositions. cast_id always has 8 digits, cast_person_id always has 7 or less digits. 
        Therefore if cast_id has 7 digits, it was probably switched.
        """
        both_numeric = self.dataset[self.dataset['cast_id'].apply(is_a_number) & self.dataset['cast_person_id'].apply(is_a_number)]
        rainfall_contains_153712 = both_numeric[both_numeric['cast_id'].astype(str).str.len() != 8]
        self._label_word_transpositions(column_names=["cast_id", "cast_person_id"], row_indices=rainfall_contains_153712.index)