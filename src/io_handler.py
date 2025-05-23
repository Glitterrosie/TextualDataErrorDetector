import os

import pandas as pd
from error_types import ErrorType


class IOHandler():
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path


    def import_dataset(self) -> pd.DataFrame:
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset path {self.dataset_path} does not exist.")
        dataset = pd.read_csv(self.dataset_path)
        return dataset


    def export_labels(self, labels: pd.DataFrame):
        self._print_percentage_of_labeled_cells(labels)

        output_folder = os.path.dirname(self.dataset_path)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        base_name, ext = os.path.splitext(os.path.basename(self.dataset_path))
        labels_base_name = base_name + '_error_mappings'

        labels_output_path = os.path.join(output_folder, f"{labels_base_name}{ext}")
        labels.to_csv(labels_output_path, index=False)


    def _print_percentage_of_labeled_cells(self, labels: pd.DataFrame) -> float:
        """
        Returns the percentage of polluted cells in the dataset.
        """
        total_cells = labels.size
        num_typos = labels.eq(ErrorType.TYPO.value).sum().sum()
        num_misspellings = labels.eq(ErrorType.MISSPELLING.value).sum().sum()
        num_ocrs = labels.eq(ErrorType.OCR.value).sum().sum()
        num_word_transpositions = labels.eq(ErrorType.WORD_TRANSPOSITION.value).sum().sum()
        num_labeled_cells = num_typos + num_misspellings + num_ocrs + num_word_transpositions
        num_labeled_rows = labels.ne(0).any(axis=1).sum()

        print(f"Number of labeled cells: {num_labeled_cells}, Number of labeled rows: {num_labeled_rows}")
        print(f"Percentage of polluted cells: \t\t{num_labeled_cells / total_cells * 100:.2f}%")
        print(f"Percentage of typo cells: \t\t{num_typos / total_cells * 100:.2f}%")
        print(f"Percentage of misspelling cells: \t{num_misspellings / total_cells * 100:.2f}%")
        print(f"Percentage of OCR cells: \t\t{num_ocrs / total_cells * 100:.2f}%")
        print(f"Percentage of transposition cells: \t{num_word_transpositions / total_cells * 100:.2f}%\n\n")
