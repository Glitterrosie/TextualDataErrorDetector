from functools import partial

from detector import Detector
from utils.generic_label_utils import check_with_spelling_library, is_not_a_number
from utils.specific_label_utils import (
    differentiate_errors_in_categorical_columns,
    set_all_labels_to_ocr,
)


class MedicalDetector(Detector):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)

    def detect(self):
        print(f"--- Medical Diabetes Dataset ---")
        print(f"Number of cells: {self.dataset.size}, Number of rows: {self.dataset.shape[0]}")

        super().detect()

    def get_column_generic_label_mapping(self) -> dict:
        return {
            "encounter_id": is_not_a_number,
            "patient_nbr": is_not_a_number,
            "race": check_with_spelling_library,
            "gender": check_with_spelling_library,
            "age": is_not_a_number,
            "weight": is_not_a_number,
            "admission_type_id": is_not_a_number,
            "discharge_disposition_id": is_not_a_number,
            "admission_source_id": is_not_a_number,
            "time_in_hospital": is_not_a_number,
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
            "max_glu_serum": check_with_spelling_library,
            "A1Cresult": check_with_spelling_library,
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
        no_steady_up_down_func = partial(differentiate_errors_in_categorical_columns, categorical_values_list=['No', 'Steady', 'Up', 'Down'])

        return {
            "encounter_id": set_all_labels_to_ocr,
            "patient_nbr": set_all_labels_to_ocr,
            "race": differentiate_errors_in_categorical_columns,
            "gender": set_all_labels_to_ocr, # we checked manually that all values are caused by OCR errors
            "age": set_all_labels_to_ocr,
            "weight": set_all_labels_to_ocr,
            "admission_type_id": set_all_labels_to_ocr,
            "discharge_disposition_id": set_all_labels_to_ocr,
            "admission_source_id": set_all_labels_to_ocr,
            "time_in_hospital": set_all_labels_to_ocr,
            "payer_code": set_all_labels_to_ocr, # we checked manually that all values that are not 'MC' are caused by OCR errors
            "medical_specialty": differentiate_errors_in_categorical_columns,
            "num_lab_procedures": set_all_labels_to_ocr,
            "num_procedures": set_all_labels_to_ocr,
            "num_medications": set_all_labels_to_ocr,
            "number_outpatient": set_all_labels_to_ocr,
            "number_emergency": set_all_labels_to_ocr,
            "number_inpatient": set_all_labels_to_ocr,
            "diag_1": set_all_labels_to_ocr,
            "diag_2": differentiate_errors_in_categorical_columns,
            "diag_3": differentiate_errors_in_categorical_columns,
            "number_diagnoses": differentiate_errors_in_categorical_columns,
            "max_glu_serum": differentiate_errors_in_categorical_columns,
            "A1Cresult": differentiate_errors_in_categorical_columns,
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
            "change": differentiate_errors_in_categorical_columns,
            "diabetesMed": differentiate_errors_in_categorical_columns,
            "readmitted": differentiate_errors_in_categorical_columns,
            "admission_type_desc": differentiate_errors_in_categorical_columns,
            "admission_source_desc": differentiate_errors_in_categorical_columns,
            "discharge_disposition_desc": differentiate_errors_in_categorical_columns,
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


