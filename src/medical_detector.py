from functools import partial

from detector import Detector
from constants import MEDICAL_SPECIALTY_VALUES
from utils.generic_label_utils import check_with_spelling_library, is_not_a_number, is_not_a_number_in_range
from utils.specific_label_utils import (
    differentiate_errors_in_number_column,
    differentiate_errors_in_string_column,
    set_all_labels_to_ocr,
)


class MedicalDetector(Detector):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)

    def detect(self):
        print(f"--- Medical Diabetes Dataset ---")
        print(f"Number of cells: {self.dataset.size}, Number of rows: {self.dataset.shape[0]}")

        super().detect()
        self._label_diabetesMed_change_transpositions()

    def get_column_generic_label_mapping(self) -> dict:
        return {
            "encounter_id": is_not_a_number,
            "patient_nbr": is_not_a_number,
            "race": self._is_not_a_valid_race,
            "gender": self._is_not_male_female,
            "age": is_not_a_number,
            "weight": is_not_a_number,
            "admission_type_id": is_not_a_number,
            "discharge_disposition_id": is_not_a_number,
            "admission_source_id": is_not_a_number,
            "time_in_hospital": partial(is_not_a_number_in_range, min_value=0, max_value=30),
            "payer_code": self._check_payer_code_is_MC,
            "medical_specialty": check_with_spelling_library,
            "num_lab_procedures": is_not_a_number,
            "num_procedures": is_not_a_number,
            "num_medications": is_not_a_number,
            "number_outpatient": is_not_a_number,
            "number_emergency": is_not_a_number,
            "number_inpatient": is_not_a_number,
            "diag_1": is_not_a_number,
            "diag_2": check_with_spelling_library,
            "diag_3": check_with_spelling_library,
            "number_diagnoses": check_with_spelling_library,
            "max_glu_serum": self._not_a_max_glu_serum,
            "A1Cresult": self._not_a_a1c_result,
            "metformin": self._check_not_in_No_Steady_Up_Down,
            "repaglinide": self._check_not_in_No_Steady_Up_Down,
            "nateglinide": self._check_not_in_No_Steady_Up_Down,
            "chlorpropamide": self._check_not_in_No_Steady_Up_Down,
            "glimepiride": self._check_not_in_No_Steady_Up_Down,
            "acetohexamide": self._check_not_in_No_Steady_Up_Down,
            "glipizide": self._check_not_in_No_Steady_Up_Down,
            "glyburide": self._check_not_in_No_Steady_Up_Down,
            "tolbutamide": self._check_not_in_No_Steady_Up_Down,
            "pioglitazone": self._check_not_in_No_Steady_Up_Down,
            "rosiglitazone": self._check_not_in_No_Steady_Up_Down,
            "acarbose": self._check_not_in_No_Steady_Up_Down,
            "miglitol": self._check_not_in_No_Steady_Up_Down,
            "troglitazone": self._check_not_in_No_Steady_Up_Down,
            "tolazamide": self._check_not_in_No_Steady_Up_Down,
            "examide": self._check_not_in_No_Steady_Up_Down,
            "citoglipton": self._check_not_in_No_Steady_Up_Down,
            "insulin": self._check_not_in_No_Steady_Up_Down,
            "glyburide-metformin": self._check_not_in_No_Steady_Up_Down,
            "glipizide-metformin": self._check_not_in_No_Steady_Up_Down,
            "glimepiride-pioglitazone": self._check_not_in_No_Steady_Up_Down,
            "metformin-rosiglitazone": self._check_not_in_No_Steady_Up_Down,
            "metformin-pioglitazone": self._check_not_in_No_Steady_Up_Down,
            "change": check_with_spelling_library,
            "diabetesMed": check_with_spelling_library,
            "readmitted": check_with_spelling_library,
            "admission_type_desc": check_with_spelling_library,
            "admission_source_desc": check_with_spelling_library,
            "discharge_disposition_desc": check_with_spelling_library,
        }


    def get_column_specific_label_mapping(self) -> dict:
        # TODO: using a categorical_values_list greatly DECREASES the number of typos and misspelings and INCREASES the number of OCR errors, check if this is correct
        no_steady_up_down_func = partial(differentiate_errors_in_string_column, categorical_values=['No', 'Steady', 'Up', 'Down'])
        medical_specialty_func = partial(differentiate_errors_in_string_column, categorical_values=MEDICAL_SPECIALTY_VALUES)

        return {
            "encounter_id": set_all_labels_to_ocr,                      # IDs have no typos -> OCR
            "patient_nbr": set_all_labels_to_ocr,                       # IDs have no typos -> OCR
            "race": set_all_labels_to_ocr,                              # Manual check -> all OCRs
            "gender": set_all_labels_to_ocr,                            # Manual check -> all OCRs
            "age": differentiate_errors_in_number_column,               # TODO: likely no typos
            "weight": differentiate_errors_in_number_column,            # TODO: likely no typos
            "admission_type_id": set_all_labels_to_ocr,                 # IDs have no typos -> OCR
            "discharge_disposition_id": set_all_labels_to_ocr,          # IDs have no typos -> OCR
            "admission_source_id": set_all_labels_to_ocr,               # IDs have no typos -> OCR
            "time_in_hospital": partial(differentiate_errors_in_number_column, min_value=0, max_value=30), # results in only OCRs
            "payer_code": set_all_labels_to_ocr,                        # Manual check -> all OCRs
            "medical_specialty": medical_specialty_func,
            "num_lab_procedures": set_all_labels_to_ocr,
            "num_procedures": set_all_labels_to_ocr,
            "num_medications": set_all_labels_to_ocr,
            "number_outpatient": set_all_labels_to_ocr,
            "number_emergency": set_all_labels_to_ocr,
            "number_inpatient": set_all_labels_to_ocr,
            "diag_1": set_all_labels_to_ocr,
            "diag_2": differentiate_errors_in_string_column,
            "diag_3": differentiate_errors_in_string_column,
            "number_diagnoses": differentiate_errors_in_string_column,
            "max_glu_serum": set_all_labels_to_ocr,
            "A1Cresult": set_all_labels_to_ocr,
            "metformin": no_steady_up_down_func, 
            "nateglinide": no_steady_up_down_func,
            "repaglinide": no_steady_up_down_func,
            "chlorpropamide": no_steady_up_down_func,
            "glimepiride": no_steady_up_down_func,
            "acetohexamide": no_steady_up_down_func,
            "glipizide": no_steady_up_down_func,
            "glyburide": no_steady_up_down_func,
            "tolbutamide": no_steady_up_down_func,
            "pioglitazone": no_steady_up_down_func,
            "rosiglitazone": no_steady_up_down_func,
            "acarbose": no_steady_up_down_func,
            "miglitol": no_steady_up_down_func,
            "troglitazone": no_steady_up_down_func,
            "tolazamide": no_steady_up_down_func,
            "examide": no_steady_up_down_func,
            "citoglipton": no_steady_up_down_func,
            "insulin": no_steady_up_down_func,
            "glyburide-metformin": no_steady_up_down_func,
            "glipizide-metformin": no_steady_up_down_func,
            "glimepiride-pioglitazone": no_steady_up_down_func,
            "metformin-rosiglitazone": no_steady_up_down_func,
            "metformin-pioglitazone": no_steady_up_down_func,
            "change": differentiate_errors_in_string_column,
            "diabetesMed": differentiate_errors_in_string_column,
            "readmitted": differentiate_errors_in_string_column,
            "admission_type_desc": differentiate_errors_in_string_column,
            "admission_source_desc": differentiate_errors_in_string_column,
            "discharge_disposition_desc": differentiate_errors_in_string_column,
        }
    
    def _check_payer_code_is_MC(self, payer_code: str) -> bool:
        """
        Check if the payer code is 'MC' (Medicare).
        It returns 1, if the payer code is not 'MC', otherwise it returns 0.
        """
        return not payer_code.strip().upper() == "MC"

    def _check_not_in_No_Steady_Up_Down(self, word: str) -> bool:
        """
        Check if the word is not in the '[No, Steady, Up, Down]' list.
        It returns the misspelled word, if it is not in the list (invalid), otherwise it returns 0 (valid).
        """
        if not str(word).strip() in ['No', 'Steady', 'Up', 'Down']:
            return word
        return 0

    def _not_a_max_glu_serum(self, word: str) -> bool:
        if not str(word).strip() in ['Norm', 'Not Available', '>200', '>300']:
            return word
        return 0
    
    def _not_a_a1c_result(self, word:str) -> bool:
        if not str(word).strip() in ['Norm','Not Available', '>7', '>8']:
            return word
        return 0

    def _is_not_a_valid_race(self, race: str) -> bool:
        """
        Check if the race is not a valid race.
        It returns 1, if the race is not a valid race, otherwise it returns 0.
        """
        return not str(race) in ['Caucasian', 'AfricanAmerican', 'Asian', 'Hispanic', 'Other']

    def _is_not_male_female(self, gender: str) -> bool:
        """
        Check if the gender is not a valid gender.
        It returns 1, if the gender is not a valid gender, otherwise it returns 0.
        """
        return not str(gender) in ['Male', 'Female']

    def _label_diabetesMed_change_transpositions(self):
        """
        The diabetesMed and change columns have transpositions. The rule we found is that if Ch appears in the diabetesMed column,
        the columns are probably switched.
        """
        change_in_diabetes_med = self.dataset[self.dataset['diabetesMed'] == "Ch"]
        self._label_word_transpositions(column_names=["diabetesMed", "change"], row_indices=change_in_diabetes_med.index)
