from functools import partial

from error_types import ErrorType
from detector import Detector
from constants import VALID_WIND_DIRECTIONS, get_australian_cities_list
from utils.generic_label_utils import (
    is_a_number,
    is_not_a_number,
    is_not_a_number_in_range,
    is_not_value_in_list,
)
from utils.specific_label_utils import (
    differentiate_errors_in_number_column,
    differentiate_errors_in_string_column,
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

        # we know there aren't any spelling mistakes in weather, therefore we reset the wrongly labeled words
        self.labels = self.labels.replace(ErrorType.MISSPELLING.value, ErrorType.NO_ERROR.value)

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
        is_not_a_valid_wind_dir = partial(is_not_value_in_list, categorical_values_list=VALID_WIND_DIRECTIONS)
        is_not_yes_no = partial(is_not_value_in_list, categorical_values_list=['Yes', 'No'])
        is_not_valid_cloud_cover = partial(is_not_a_number_in_range, min_value=0, max_value=9)
        is_not_valid_temp = partial(is_not_a_number_in_range, min_value=-23, max_value=51)
        is_not_valid_wind_speed = partial(is_not_a_number_in_range, min_value=0, max_value=140)
        is_not_valid_sunshine = partial(is_not_a_number_in_range, min_value=0, max_value=15)
        is_not_valid_humidity = partial(is_not_a_number_in_range, min_value=0, max_value=100)

        location_list = get_australian_cities_list()
        is_not_valid_location = partial(is_not_value_in_list, categorical_values_list=location_list)

        return {
            "Date": self._is_not_a_valid_date,
            "Location": is_not_valid_location,
            "MinTemp": is_not_valid_temp,
            "MaxTemp": is_not_valid_temp,
            "Rainfall": is_not_a_number,
            "Evaporation":is_not_a_number,
            "Sunshine": is_not_valid_sunshine,
            "WindGustDir":  is_not_a_valid_wind_dir,
            "WindGustSpeed": is_not_valid_wind_speed,
            "WindDir9am": is_not_a_valid_wind_dir,
            "WindDir3pm": is_not_a_valid_wind_dir,
            "WindSpeed9am": is_not_valid_wind_speed,
            "WindSpeed3pm": is_not_valid_wind_speed,
            "Humidity9am": is_not_valid_humidity,
            "Humidity3pm": is_not_valid_humidity,
            "Pressure9am": self._is_not_valid_pressure,
            "Pressure3pm": self._is_not_valid_pressure,
            "Cloud9am": is_not_valid_cloud_cover,
            "Cloud3pm": is_not_valid_cloud_cover,
            "Temp9am": is_not_valid_temp,
            "Temp3pm": is_not_valid_temp,
            "RainToday": is_not_yes_no,
            "RainTomorrow": is_not_yes_no,
        }

    def get_column_specific_label_mapping(self) -> dict:
        location_list = get_australian_cities_list()
        differentiate_errors_for_location = partial(differentiate_errors_in_string_column, categorical_values=location_list)
        differentiate_errors_for_cloud_cover = partial(differentiate_errors_in_number_column, min_value=0, max_value=9)
        differentiate_errors_for_temp = partial(differentiate_errors_in_number_column, min_value=-23, max_value=51)
        differentiate_errors_for_wind_speed = partial(differentiate_errors_in_number_column, min_value=0, max_value=140)
        differentiate_errors_for_sunshine = partial(differentiate_errors_in_number_column, min_value=0, max_value=15)
        differentiate_errors_for_humidity = partial(differentiate_errors_in_number_column, min_value=0, max_value=100)

        return {
            "Date": set_all_labels_to_ocr,
            "Location": differentiate_errors_for_location,
            "MinTemp": differentiate_errors_for_temp,
            "MaxTemp": differentiate_errors_for_temp,
            "Rainfall": differentiate_errors_in_number_column,
            "Evaporation": differentiate_errors_in_number_column,
            "Sunshine": differentiate_errors_for_sunshine,
            "WindGustDir": set_all_labels_to_ocr,                       # Manual check -> all OCRs
            "WindGustSpeed": differentiate_errors_for_wind_speed,
            "WindDir9am": set_all_labels_to_ocr,                        # Manual check -> all OCRs
            "WindDir3pm": set_all_labels_to_ocr,                        # Manual check -> all OCRs
            "WindSpeed9am": differentiate_errors_for_wind_speed,
            "WindSpeed3pm": differentiate_errors_for_wind_speed,
            "Humidity9am": differentiate_errors_for_humidity,
            "Humidity3pm": differentiate_errors_for_humidity,
            "Pressure9am": set_all_labels_to_ocr,                       # when running the differentiate_errors_in_number_column method, we found that all values which were labeled as typos were actually OCRs
            "Pressure3pm": set_all_labels_to_ocr,                       # when running the differentiate_errors_in_number_column method, we found that all values which were labeled as typos were actually OCRs
            "Cloud9am": differentiate_errors_for_cloud_cover,
            "Cloud3pm": differentiate_errors_for_cloud_cover,
            "Temp9am": differentiate_errors_for_temp,
            "Temp3pm": differentiate_errors_for_temp,
            "RainToday": set_all_labels_to_ocr,                         # Manual check -> all OCRs
            "RainTomorrow": set_all_labels_to_ocr,                      # Manual check -> all OCRs
        }

    def _is_not_a_valid_date(self, value) -> bool:
        """
        Check if the value is not a valid date.
        The date is in format "YYYY-MM-DD".
        """
        if not isinstance(value, str):
            return value
        parts = value.split("-")
        if len(parts) != 3:
            return value
        year, month, day = parts
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return value
        if not (1 <= int(month) <= 12 and 1 <= int(day) <= 31):
            return value
        return 0

    def _is_not_valid_pressure(self, value: str) -> bool:
        """
        Check if the value is not a valid pressure.
        A valid pressure is a number between 950 and 1050.
        """
        try:
            pressure = float(value)
            return value if pressure < 950 or pressure > 1050 else 0
        except ValueError:
            return value
