from abc import ABC, abstractmethod
import pandas as pd
from io_handler import IOHandler
from error_types import ErrorType


class Detector(ABC):
    def __init__(self, dataset_path: str):
        self.io_handler = IOHandler(dataset_path)
        self.dataset = self.io_handler.import_dataset()
        self.labels = pd.DataFrame(ErrorType.NO_ERROR.value, index=self.dataset.index, columns=self.dataset.columns)
        self.generic_labeled_dataset = None

    def export(self):
        self.io_handler.export_labels(self.labels)

    def detect(self):
        """
        Detects the errors in the dataset.
        """

        self.generic_labeled_dataset = pd.DataFrame(0, index=self.dataset.index, columns=self.dataset.columns)
        column_generic_label_mapping = self.get_column_generic_label_mapping()
        for column_name in self.dataset.columns:
            #print(f"Generically labelling {column_name}")
            if column_name not in column_generic_label_mapping:
                print(f"Warning: Column '{column_name}' not found in generic label mapping. Skipping.")
                continue

            label_function = column_generic_label_mapping[column_name]

            self.generic_labeled_dataset[column_name] = self.dataset[column_name].apply(label_function)
        print("Generically labelled all data.")

        specific_column_label_mapping = self.get_column_specific_label_mapping()
        for column_name in self.dataset.columns:
            #print(f"Specifically labelling {column_name}")
            generic_labeled_cell_indices = self._get_generic_labeled_cell_indices(column_name)

            # each column has its own mapping function how to assign specific error types to the generic labeled cells
            label_function = specific_column_label_mapping[column_name]
            self.labels[column_name] = label_function(self.dataset[column_name], generic_labeled_cell_indices, self.generic_labeled_dataset[column_name])
        print("Specifically labelled all data.")

    @abstractmethod
    def get_column_generic_label_mapping(self) -> dict:
        pass

    @abstractmethod
    def get_column_specific_label_mapping(self) -> dict:
        pass

    def _get_generic_labeled_cell_indices(self, column_name: str) -> pd.Index:
        """
        Returns the indices of the cells that are labeled as generic.
        """
        if column_name not in self.generic_labeled_dataset.columns:
            raise ValueError(f"Column '{column_name}' not found in generic labeled dataset.")
        
        return self.generic_labeled_dataset[self.generic_labeled_dataset[column_name] != 0].index
