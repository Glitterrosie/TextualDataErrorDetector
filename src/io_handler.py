import os
import pickle

import pandas as pd
from tabulate import tabulate, SEPARATING_LINE

from error_types import ErrorType

total_injected_errors = {
    "imdb_subset1_group1_w_errors":
        {
        "misspellings": 215010,
        "typos": 240668,
        "ocrs": 196455,
        "transpositions": 216000
        },
    "weather_subset1_group1_w_errors":
        {
        "misspellings": 0,
        "typos": 19118,
        "ocrs": 38899,
        "transpositions": 73538
        },
    "medical_subset1_group1_w_errors":
        {
        "misspellings": 22574,
        "typos": 14937,
        "ocrs": 43959,
        "transpositions": 129452
        },
}


class IOHandler():
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path


    def import_dataset(self) -> pd.DataFrame:
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset path {self.dataset_path} does not exist.")
        dataset = pd.read_csv(self.dataset_path)
        return dataset


    def export_labels(self, labels: pd.DataFrame):

        output_folder = os.path.dirname(self.dataset_path)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        base_name, ext = os.path.splitext(os.path.basename(self.dataset_path))
        if "w_errors" in base_name:
            labels_base_name = base_name.replace("w_errors", "error_mappings")
        else:
            labels_base_name = base_name + "_error_mappings"

        labels_output_path = os.path.join(output_folder, f"{labels_base_name}{ext}")
        labels.to_csv(labels_output_path, index=False)

        self._print_percentage_of_labeled_cells(labels, base_name)


    def _print_percentage_of_labeled_cells(self, labels: pd.DataFrame, base_name: str) -> float:
        """
        Returns the percentage of polluted cells in the dataset and prints a formatted table of statistics.
        """
        total_cells = labels.size
        num_typos = int(labels.eq(ErrorType.TYPO.value).sum().sum())
        num_misspellings = int(labels.eq(ErrorType.MISSPELLING.value).sum().sum())
        num_ocrs = int(labels.eq(ErrorType.OCR.value).sum().sum())
        num_word_transpositions = int(labels.eq(ErrorType.WORD_TRANSPOSITION.value).sum().sum())
        num_labeled_cells = num_typos + num_misspellings + num_ocrs + num_word_transpositions

        true_typos = total_injected_errors[base_name]["typos"]
        true_misspellings = total_injected_errors[base_name]["misspellings"]
        true_ocrs = total_injected_errors[base_name]["ocrs"]
        true_transpositions = total_injected_errors[base_name]["transpositions"]
        total_true_errors = true_typos + true_misspellings + true_ocrs + true_transpositions

        # Prepare table data
        headers = ["Error Type", "Detected", "True Total", "Detection Rate", "% of Total Cells"]
        table_data = [
            ["Misspellings", num_misspellings, true_misspellings, f"{(num_misspellings/true_misspellings*100):.2f}%" if true_misspellings > 0 else "N/A", f"{(num_misspellings/total_cells*100):.2f}%"],
            ["Typos", num_typos, true_typos, f"{(num_typos/true_typos*100):.2f}%", f"{(num_typos/total_cells*100):.2f}%"],
            ["OCR Errors", num_ocrs, true_ocrs, f"{(num_ocrs/true_ocrs*100):.2f}%", f"{(num_ocrs/total_cells*100):.2f}%"],
            ["Word Transpositions", num_word_transpositions, true_transpositions, f"{(num_word_transpositions/true_transpositions*100):.2f}%", f"{(num_word_transpositions/total_cells*100):.2f}%"],
            ["Total", num_labeled_cells, total_true_errors, f"{(num_labeled_cells/total_true_errors*100):.2f}%", f"{(num_labeled_cells/total_cells*100):.2f}%"]
        ]

        print("\nError Detection Statistics:")
        print(tabulate(table_data, 
                      headers=headers, 
                      tablefmt="fancy_grid", 
                      numalign="right",
                      stralign="right",
                      colalign=("left", "right", "right", "right", "right"),
                      intfmt=","))
        print()


    def save_pickled_dataset(self, dataset: pd.DataFrame):
        output_folder = os.path.dirname(self.dataset_path)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        base_name, ext = os.path.splitext(os.path.basename(self.dataset_path))
        dataset_name = base_name.split('_')[0]
        pickle_name = dataset_name + '_tokenized' 

        dataset_output_path = os.path.join(output_folder, f"{pickle_name}.pkl")
        with open(dataset_output_path, 'wb') as f:
            pickle.dump(dataset, f)


    def load_pickled_dataset(self) -> pd.DataFrame:
        base_name, ext = os.path.splitext(os.path.basename(self.dataset_path))
        dataset_name = base_name.split('_')[0]
        pickle_name = dataset_name + '_tokenized' 

        dataset_output_path = os.path.join(os.path.dirname(self.dataset_path), f"{pickle_name}.pkl")
        if not os.path.exists(dataset_output_path):
            raise FileNotFoundError(f"Pickle file {dataset_output_path} does not exist.")
        
        with open(dataset_output_path, 'rb') as f:
            dataset = pickle.load(f)
        return dataset
