from functools import partial

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

VALID_WIND_DIRECTIONS = {
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
}


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
            "Date": self._is_not_a_valid_date,
            "Location": check_with_spelling_library,
            "MinTemp": is_not_a_number,
            "MaxTemp": is_not_a_number,
            "Rainfall": is_not_a_number,
            "Evaporation":is_not_a_number,
            "Sunshine": is_not_a_number,
            "WindGustDir":  self._is_not_valid_wind_dir,
            "WindGustSpeed": is_not_a_number,
            "WindDir9am": self._is_not_valid_wind_dir,
            "WindDir3pm": self._is_not_valid_wind_dir,
            "WindSpeed9am": is_not_a_number,
            "WindSpeed3pm": is_not_a_number,
            "Humidity9am": is_not_a_number,
            "Humidity3pm": is_not_a_number,
            "Pressure9am": self._is_not_valid_pressure,
            "Pressure3pm": self._is_not_valid_pressure,
            "Cloud9am": is_not_a_number,
            "Cloud3pm": is_not_a_number,
            "Temp9am": is_not_a_number,
            "Temp3pm": is_not_a_number,
            "RainToday": self._is_not_yes_no,
            "RainTomorrow": self._is_not_yes_no,
        }

    def get_column_specific_label_mapping(self) -> dict:
        wind_dir_function = partial(differentiate_errors_in_categorical_columns, categorical_values=VALID_WIND_DIRECTIONS)
        yes_no_function = partial(differentiate_errors_in_categorical_columns, categorical_values=["Yes", "No"])

        return {
            "Date": set_all_labels_to_ocr,
            "Location": differentiate_errors_in_categorical_columns,
            "MinTemp": set_all_labels_to_ocr,
            "MaxTemp": set_all_labels_to_ocr,
            "Rainfall": set_all_labels_to_ocr,
            "Evaporation": set_all_labels_to_ocr,
            "Sunshine": set_all_labels_to_ocr,
            "WindGustDir": wind_dir_function,
            "WindGustSpeed": set_all_labels_to_ocr,
            "WindDir9am": wind_dir_function,
            "WindDir3pm": wind_dir_function,
            "WindSpeed9am": set_all_labels_to_ocr,
            "WindSpeed3pm": set_all_labels_to_ocr,
            "Humidity9am": set_all_labels_to_ocr,
            "Humidity3pm": set_all_labels_to_ocr,
            "Pressure9am": set_all_labels_to_ocr, # TODO: do not set all to OCR, but also check for typos
            "Pressure3pm": set_all_labels_to_ocr,
            "Cloud9am": set_all_labels_to_ocr,
            "Cloud3pm": set_all_labels_to_ocr,
            "Temp9am": set_all_labels_to_ocr,
            "Temp3pm": set_all_labels_to_ocr,
            "RainToday": yes_no_function,
            "RainTomorrow": yes_no_function,
        }

    def _is_not_a_valid_date(self, value: str) -> bool:
        """
        Check if the value is not a valid date.
        The date is in format "YYYY-MM-DD".
        """
        if not isinstance(value, str):
            return True
        parts = value.split("-")
        if len(parts) != 3:
            return True
        year, month, day = parts
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return True
        if not (1 <= int(month) <= 12 and 1 <= int(day) <= 31):
            return True
        return False

    def _is_not_valid_wind_dir(self, value: str) -> bool:
        """
        Check if the wind gust direction is not a valid direction.
        Valid directions are: N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW.
        """
        return value if value not in VALID_WIND_DIRECTIONS else False

    def _is_not_yes_no(self, value: str) -> bool:
        """
        Check if the value is not 'Yes' or 'No'.
        """
        return value if value not in ["Yes", "No"] else False

    def _is_not_valid_pressure(self, value: str) -> bool:
        """
        Check if the value is not a valid pressure.
        A valid pressure is a number between 950 and 1050.
        """
        try:
            pressure = float(value)
            return value if pressure < 950 or pressure > 1050 else False
        except ValueError:
            return value
