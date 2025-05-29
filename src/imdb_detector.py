from detector import Detector
from utils.generic_label_utils import empty_method, is_not_a_number, has_a_typo_or_misspelling
from utils.specific_label_utils import no_labels, set_all_labels_to_ocr, differentiate_mistakes_in_categorical_columns



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
            "cast_person_role_id": has_a_typo_or_misspelling,
            "cast_note": has_a_typo_or_misspelling,
            "cast_nr_order": is_not_a_number,
            "cast_role_id": is_not_a_number,
            "person_id": is_not_a_number,
            "person_movie_id": has_a_typo_or_misspelling,
            "person_info_type_id": is_not_a_number,
            "extra_info": has_a_typo_or_misspelling,
            "person_note": has_a_typo_or_misspelling,
            "title_id": is_not_a_number,
            "title": has_a_typo_or_misspelling,
            "imdb_index": has_a_typo_or_misspelling,
            "kind_id": is_not_a_number,
            "production_year": is_not_a_number,
            "phonetic_code": has_a_typo_or_misspelling,
            "episode_of_id": is_not_a_number,
            "season_nr": is_not_a_number,
            "episode_nr": is_not_a_number,
            "series_years": is_not_a_number,
            "md5sum": has_a_typo_or_misspelling,
            "name": has_a_typo_or_misspelling,
        }


    def get_column_specific_label_mapping(self) -> dict:
        return {
            "cast_id": set_all_labels_to_ocr,
            "cast_person_id": set_all_labels_to_ocr,
            "cast_movie_id": set_all_labels_to_ocr,
            "cast_person_role_id": differentiate_mistakes_in_categorical_columns,
            "cast_note": differentiate_mistakes_in_categorical_columns,
            "cast_nr_order": set_all_labels_to_ocr,
            "cast_role_id": set_all_labels_to_ocr,
            "person_id": set_all_labels_to_ocr,
            "person_movie_id": differentiate_mistakes_in_categorical_columns,
            "person_info_type_id": set_all_labels_to_ocr,
            "extra_info": differentiate_mistakes_in_categorical_columns,
            "person_note": differentiate_mistakes_in_categorical_columns,
            "title_id": set_all_labels_to_ocr,
            "title": differentiate_mistakes_in_categorical_columns,
            "imdb_index": differentiate_mistakes_in_categorical_columns,
            "kind_id": set_all_labels_to_ocr,
            "production_year": set_all_labels_to_ocr,
            "phonetic_code": differentiate_mistakes_in_categorical_columns,
            "episode_of_id": set_all_labels_to_ocr,
            "season_nr": set_all_labels_to_ocr,
            "episode_nr": set_all_labels_to_ocr,
            "series_years": set_all_labels_to_ocr,
            "md5sum": differentiate_mistakes_in_categorical_columns,
            "name": differentiate_mistakes_in_categorical_columns,
        }

