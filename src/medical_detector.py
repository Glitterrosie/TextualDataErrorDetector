from functools import partial

from detector import Detector
from constants.categorical_values import DISCHARGE_DISPOSITION_DESC_VALUES, ADMISSION_TYPE_DESC_VALUES, ADMISSION_SOURCE_DESC_VALUES, MEDICAL_SPECIALTY_VALUES
from utils.generic_label_utils import check_with_spelling_library, is_a_number, is_not_a_number, is_not_a_number_in_range, is_not_value_in_list
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
        self._label_num_procedures_num_medications_transpositions()

    def get_column_generic_label_mapping(self) -> dict:
        is_not_a_valid_race = partial(is_not_value_in_list, categorical_values_list=['Caucasian', 'AfricanAmerican', 'Asian', 'Hispanic', 'Other'])
        is_not_a_valid_gender = partial(is_not_value_in_list, categorical_values_list=['Male', 'Female', 'Unknown/Invalid'])
        is_not_in_no_steady_up_down = partial(is_not_value_in_list, categorical_values_list=['No', 'Steady', 'Up', 'Down'])
        is_not_a_valid_medical_specialty = partial(is_not_value_in_list, categorical_values_list=MEDICAL_SPECIALTY_VALUES)
        is_not_a_valid_admission_type_desc = partial(is_not_value_in_list, categorical_values_list=ADMISSION_TYPE_DESC_VALUES)
        is_not_a_valid_admission_source_desc = partial(is_not_value_in_list, categorical_values_list=ADMISSION_SOURCE_DESC_VALUES)
        is_not_a_valid_discharge_disposition_desc = partial(is_not_value_in_list, categorical_values_list=DISCHARGE_DISPOSITION_DESC_VALUES)
        is_not_a_valid_max_glu_serum = partial(is_not_value_in_list, categorical_values_list=['Norm', 'Not Available', '>200', '>300'])
        is_not_a_valid_a1c_result = partial(is_not_value_in_list, categorical_values_list=['Norm','Not Available', '>7', '>8'])
        is_not_a_valid_readmitted = partial(is_not_value_in_list, categorical_values_list=['No', '<30', '>30'])
        is_not_a_valid_change = partial(is_not_value_in_list, categorical_values_list=['No', 'Ch', 'Gli'])
        is_not_a_valid_diabetes_med = partial(is_not_value_in_list, categorical_values_list=['Yes', 'No'])

        return {
            "encounter_id": is_not_a_number,
            "patient_nbr": is_not_a_number,
            "race": is_not_a_valid_race,
            "gender": is_not_a_valid_gender,
            "age": is_not_a_number,
            "weight": is_not_a_number,
            "admission_type_id": partial(is_not_a_number_in_range, min_value=0, max_value=9),
            "discharge_disposition_id": partial(is_not_a_number_in_range, min_value=0, max_value=29),
            "admission_source_id": partial(is_not_a_number_in_range, min_value=0, max_value=19),
            "time_in_hospital": partial(is_not_a_number_in_range, min_value=0, max_value=30),
            "payer_code": self._check_payer_code_is_MC,
            "medical_specialty": is_not_a_valid_medical_specialty,
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
            "max_glu_serum": is_not_a_valid_max_glu_serum,
            "A1Cresult": is_not_a_valid_a1c_result,
            "metformin": is_not_in_no_steady_up_down,
            "repaglinide": is_not_in_no_steady_up_down,
            "nateglinide": is_not_in_no_steady_up_down,
            "chlorpropamide": is_not_in_no_steady_up_down,
            "glimepiride": is_not_in_no_steady_up_down,
            "acetohexamide": is_not_in_no_steady_up_down,
            "glipizide": is_not_in_no_steady_up_down,
            "glyburide": is_not_in_no_steady_up_down,
            "tolbutamide": is_not_in_no_steady_up_down,
            "pioglitazone": is_not_in_no_steady_up_down,
            "rosiglitazone": is_not_in_no_steady_up_down,
            "acarbose": is_not_in_no_steady_up_down,
            "miglitol": is_not_in_no_steady_up_down,
            "troglitazone": is_not_in_no_steady_up_down,
            "tolazamide": is_not_in_no_steady_up_down,
            "examide": is_not_in_no_steady_up_down,
            "citoglipton": is_not_in_no_steady_up_down,
            "insulin": is_not_in_no_steady_up_down,
            "glyburide-metformin": is_not_in_no_steady_up_down,
            "glipizide-metformin": is_not_in_no_steady_up_down,
            "glimepiride-pioglitazone": is_not_in_no_steady_up_down,
            "metformin-rosiglitazone": is_not_in_no_steady_up_down,
            "metformin-pioglitazone": is_not_in_no_steady_up_down,
            "change": is_not_a_valid_change,
            "diabetesMed": is_not_a_valid_diabetes_med,
            "readmitted": is_not_a_valid_readmitted,
            "admission_type_desc": is_not_a_valid_admission_type_desc,
            "admission_source_desc": is_not_a_valid_admission_source_desc,
            "discharge_disposition_desc": is_not_a_valid_discharge_disposition_desc,
        }


    def get_column_specific_label_mapping(self) -> dict:
        # TODO: using a categorical_values_list greatly DECREASES the number of typos and misspelings and INCREASES the number of OCR errors, check if this is correct
        no_steady_up_down_func = partial(differentiate_errors_in_string_column, categorical_values=['No', 'Steady', 'Up', 'Down'])
        medical_specialty_func = partial(differentiate_errors_in_string_column, categorical_values=MEDICAL_SPECIALTY_VALUES)
        admission_type_desc_func = partial(differentiate_errors_in_string_column, categorical_values=ADMISSION_TYPE_DESC_VALUES)
        admission_source_desc_func = partial(differentiate_errors_in_string_column, categorical_values=ADMISSION_SOURCE_DESC_VALUES)
        discharge_disposition_desc_func = partial(differentiate_errors_in_string_column, categorical_values=DISCHARGE_DISPOSITION_DESC_VALUES)

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
            "readmitted": set_all_labels_to_ocr,                        # Manual check -> all OCRs
            "admission_type_desc": admission_type_desc_func,
            "admission_source_desc": admission_source_desc_func,
            "discharge_disposition_desc": discharge_disposition_desc_func,
        }

    def _check_payer_code_is_MC(self, payer_code: str) -> bool:
        """
        Check if the payer code is 'MC' (Medicare).
        It returns 1, if the payer code is not 'MC', otherwise it returns 0.
        """
        return payer_code if not payer_code.strip().upper() == "MC" else 0


    def _label_diabetesMed_change_transpositions(self):
        """
        The diabetesMed and change columns have transpositions. The rule we found is that if Ch appears in the diabetesMed column,
        the columns are probably switched.
        """
        change_in_diabetes_med = self.dataset[self.dataset['diabetesMed'] == "Ch"]
        self._label_word_transpositions(column_names=["diabetesMed", "change"], row_indices=change_in_diabetes_med.index)

    def _label_num_procedures_num_medications_transpositions(self):
        """
        Num procedures is a number, but it can only be between 0 and 12, while num_medications has a much higher value range.
        """
        both_numeric = self.dataset[self.dataset['num_procedures'].apply(is_a_number) & self.dataset['num_medications'].apply(is_a_number)]
        num_procedures_is_greater_12 = both_numeric[both_numeric['num_procedures'].astype(int) > 12]
        self._label_word_transpositions(column_names=["Rainfall", "Evaporation"], row_indices=num_procedures_is_greater_12.index)
