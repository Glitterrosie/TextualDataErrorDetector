from detector import Detector
from utils.generic_label_utils import empty_method, is_not_a_number, has_a_typo_or_misspelling
from utils.specific_label_utils import no_labels, set_all_labels_to_ocr, differentiate_mistakes_in_categorical_columns


class WeatherDetector(Detector):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)

    def detect(self):
        print(f"--- Australian Weather Dataset ---")
        print(f"Number of cells: {self.dataset.size}, Number of rows: {self.dataset.shape[0]}")

        super().detect()

    def get_column_generic_label_mapping(self) -> dict:
        return {
            "Date": empty_method,
            "Location": has_a_typo_or_misspelling,
            "MinTemp": is_not_a_number,
            "MaxTemp": is_not_a_number,
            "Rainfall": is_not_a_number,
            "Evaporation":is_not_a_number,
            "Sunshine": is_not_a_number,
            "WindGustDir":  has_a_typo_or_misspelling,
            "WindGustSpeed": is_not_a_number,
            "WindDir9am": has_a_typo_or_misspelling,
            "WindDir3pm": has_a_typo_or_misspelling,
            "WindSpeed9am": is_not_a_number,
            "WindSpeed3pm": is_not_a_number,
            "Humidity9am": is_not_a_number,
            "Humidity3pm": is_not_a_number,
            "Pressure9am": is_not_a_number,
            "Pressure3pm": is_not_a_number,
            "Cloud9am": is_not_a_number,
            "Cloud3pm": is_not_a_number,
            "Temp9am": is_not_a_number,
            "Temp3pm": is_not_a_number,
            "RainToday": has_a_typo_or_misspelling,
            "RainTomorrow": has_a_typo_or_misspelling,
        }

    def get_column_specific_label_mapping(self) -> dict:
        return {
            "Date": no_labels,
            "Location": differentiate_mistakes_in_categorical_columns,
            "MinTemp": set_all_labels_to_ocr,
            "MaxTemp": set_all_labels_to_ocr,
            "Rainfall": set_all_labels_to_ocr,
            "Evaporation": set_all_labels_to_ocr,
            "Sunshine": set_all_labels_to_ocr,
            "WindGustDir": differentiate_mistakes_in_categorical_columns,
            "WindGustSpeed": set_all_labels_to_ocr,
            "WindDir9am": differentiate_mistakes_in_categorical_columns,
            "WindDir3pm": differentiate_mistakes_in_categorical_columns,
            "WindSpeed9am": set_all_labels_to_ocr,
            "WindSpeed3pm": set_all_labels_to_ocr,
            "Humidity9am": set_all_labels_to_ocr,
            "Humidity3pm": set_all_labels_to_ocr,
            "Pressure9am": set_all_labels_to_ocr,
            "Pressure3pm": set_all_labels_to_ocr,
            "Cloud9am": set_all_labels_to_ocr,
            "Cloud3pm": set_all_labels_to_ocr,
            "Temp9am": set_all_labels_to_ocr,
            "Temp3pm": set_all_labels_to_ocr,
            "RainToday": differentiate_mistakes_in_categorical_columns,
            "RainTomorrow": differentiate_mistakes_in_categorical_columns,
        }
