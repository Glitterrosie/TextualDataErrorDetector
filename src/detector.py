from abc import ABC, abstractmethod

import pandas as pd
from error_types import ErrorType
from io_handler import IOHandler


class Detector(ABC):
    def __init__(self, dataset_path: str):
        self.io_handler = IOHandler(dataset_path)
        self.dataset = self.io_handler.import_dataset()
        self.labels = pd.DataFrame(ErrorType.NO_ERROR.value, index=self.dataset.index, columns=self.dataset.columns)


    @abstractmethod
    def detect(self):
        """
        Detects the errors in the dataset.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")


    def export(self):
        self.io_handler.export_labels(self.labels)
