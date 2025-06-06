from detector import Detector
from utils.generic_label_utils import (
    check_with_spelling_library,
    empty_method,
    is_a_number,
    is_not_a_number,
)
from utils.specific_label_utils import (
    differentiate_errors_in_categorical_columns,
    no_labels,
    set_all_labels_to_ocr,
)


class WeatherDetector(Detector):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)

    def detect(self):
        print(f"--- Australian Weather Dataset ---")
        print(f"Number of cells: {self.dataset.size}, Number of rows: {self.dataset.shape[0]}")

        super().detect()

        self._label_temperature_tranpositions()
        self._label_rainfall_evaporation_transpositions()
        self._label_sunshine_evaporation_transpositions()
        self._label_sunshine_rainfall_transpositions()

    def _label_temperature_tranpositions(self):
        """
        We label all cells as transpositions, where the minimum temperature is greater than the maximum temperature.
        """
        both_numeric = self.dataset[self.dataset['MinTemp'].apply(is_a_number) & self.dataset['MaxTemp'].apply(is_a_number)]
        min_greater_max = both_numeric[both_numeric['MinTemp'].astype(float) > both_numeric['MaxTemp'].astype(float)]
        self._label_word_transpositions(column_names=["MinTemp", "MaxTemp"], row_indices=min_greater_max.index)

    def _label_rainfall_evaporation_transpositions(self):
        """
        The rainfall and evaporation columns have transpositions, which are really hard to detect, because both are numeric and
        can be in the same value range. Because 57% of values in the evaporation column are "15.3712", and because we mostly
        observed obvious tranpositions with this value, we label all cells in the rainfall and evaporation columns as transpositions
        where rainfall = "15.3712" and evaporation is numeric.
        """
        both_numeric = self.dataset[self.dataset['Rainfall'].apply(is_a_number) & self.dataset['Evaporation'].apply(is_a_number)]
        rainfall_contains_153712 = both_numeric[both_numeric['Rainfall'].astype(float) == 15.3712]
        self._label_word_transpositions(column_names=["Rainfall", "Evaporation"], row_indices=rainfall_contains_153712.index)

    def _label_sunshine_evaporation_transpositions(self):
        """
        The sunshine and evaporation columns have transpositions, which are really hard to detect, because both are numeric and
        can be in the same value range. Because 65% of values in the sunshine column are "14.03" and 57% of values in the sunshine column
        are "15.3712", and because we mostly observed obvious tranpositions with these values, we label all cells in the sunshine and 
        evaporation columns as transpositions where evaporation = "14.03" or sunshine = "15.3712" and both columns are numeric.
        """
        both_numeric = self.dataset[self.dataset['Evaporation'].apply(is_a_number) & self.dataset['Sunshine'].apply(is_a_number)]
        switched_rows = both_numeric[
            (both_numeric['Sunshine'].astype(float) == 15.3712) | (both_numeric['Evaporation'].astype(float) == 14.03)
        ]
        self._label_word_transpositions(column_names=["Sunshine", "Evaporation"], row_indices=switched_rows.index)

    def _label_sunshine_rainfall_transpositions(self):
        """
        The sunshine and rainfall columns have transpositions, which are really hard to detect, because both are numeric and
        can be in the same value range. Because 65% of values in the sunshine column are "14.03", and because we mostly observed obvious
        tranpositions with this value, we label all cells in the sunshine and rainfall columns as transpositions where rainfall = "14.03".
        """
        both_numeric = self.dataset[self.dataset['Rainfall'].apply(is_a_number) & self.dataset['Evaporation'].apply(is_a_number)]
        rainfall_contains_1403 = both_numeric[both_numeric['Rainfall'].astype(float) == 14.03]
        self._label_word_transpositions(column_names=["Rainfall", "Evaporation"], row_indices=rainfall_contains_1403.index)


    def get_column_generic_label_mapping(self) -> dict:
        return {
            "Date": empty_method,
            "Location": check_with_spelling_library,
            "MinTemp": is_not_a_number,
            "MaxTemp": is_not_a_number,
            "Rainfall": is_not_a_number,
            "Evaporation":is_not_a_number,
            "Sunshine": is_not_a_number,
            "WindGustDir":  check_with_spelling_library,
            "WindGustSpeed": is_not_a_number,
            "WindDir9am": check_with_spelling_library,
            "WindDir3pm": check_with_spelling_library,
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
            "RainToday": check_with_spelling_library,
            "RainTomorrow": check_with_spelling_library,
        }

    def get_column_specific_label_mapping(self) -> dict:
        return {
            "Date": no_labels,
            "Location": differentiate_errors_in_categorical_columns,
            "MinTemp": set_all_labels_to_ocr,
            "MaxTemp": set_all_labels_to_ocr,
            "Rainfall": set_all_labels_to_ocr,
            "Evaporation": set_all_labels_to_ocr,
            "Sunshine": set_all_labels_to_ocr,
            "WindGustDir": differentiate_errors_in_categorical_columns,
            "WindGustSpeed": set_all_labels_to_ocr,
            "WindDir9am": differentiate_errors_in_categorical_columns,
            "WindDir3pm": differentiate_errors_in_categorical_columns,
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
            "RainToday": differentiate_errors_in_categorical_columns,
            "RainTomorrow": differentiate_errors_in_categorical_columns,
        }
