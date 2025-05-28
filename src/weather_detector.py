from detector import Detector
from utils.generic_label_utils import empty_method, is_not_a_number
from utils.specific_label_utils import no_labels, set_all_labels_to_ocr


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
            "Location": empty_method,
            "MinTemp": is_not_a_number,
            "MaxTemp": is_not_a_number,
            "Rainfall": is_not_a_number,
            "Evaporation":is_not_a_number,
            "Sunshine": is_not_a_number,
            "WindGustDir":  empty_method,
            "WindGustSpeed": is_not_a_number,
            "WindDir9am": empty_method,
            "WindDir3pm": empty_method,
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
            "RainToday": empty_method,
            "RainTomorrow": empty_method,
        }

    def get_column_specific_label_mapping(self) -> dict:
        return {
            "Date": no_labels,
            "Location": no_labels,
            "MinTemp": set_all_labels_to_ocr,
            "MaxTemp": set_all_labels_to_ocr,
            "Rainfall": set_all_labels_to_ocr,
            "Evaporation": set_all_labels_to_ocr,
            "Sunshine": set_all_labels_to_ocr,
            "WindGustDir": no_labels,
            "WindGustSpeed": set_all_labels_to_ocr,
            "WindDir9am": no_labels,
            "WindDir3pm": no_labels,
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
            "RainToday": no_labels,
            "RainTomorrow": no_labels,
        }
