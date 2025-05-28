from detector import Detector


class MedicalDetector(Detector):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)

    def detect(self):
        print(f"--- Medical Diabetes Dataset ---")
        print(f"Number of cells: {self.dataset.size}, Number of rows: {self.dataset.shape[0]}")

        super().detect()

        number_columns = ["encounter_id", "patient_nbr", "age", "weight", "admission_type_id", "discharge_disposition_id", "admission_source_id", "time_in_hospital", "num_lab_procedures", "num_procedures", "num_medications", "number_outpatient", "number_emergency", "number_inpatient", "diag_1"]
        self.check_for_ocr(number_columns)
        self.check_for_typo_vectorized()
        self.check_for_misspellings_short()

    def get_column_generic_label_mapping(self):
        pass

    def get_column_specific_label_mapping(self):
        pass
