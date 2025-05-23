import re
from abc import ABC, abstractmethod

import pandas as pd
from error_types import ErrorType
from io_handler import IOHandler


class Detector(ABC):
    def __init__(self, dataset_path: str):
        self.io_handler = IOHandler(dataset_path)
        self.dataset = self.io_handler.import_dataset()
        self.labels = pd.DataFrame(ErrorType.NO_ERROR.value, index=self.dataset.index, columns=self.dataset.columns)


    def detect(self, use_tokenized_dataset: bool = False):
        """
        Detects the errors in the dataset.
        This method should be implemented by subclasses.
        Parameters:
            :use_tokenized_dataset: If True, uses an already tokenized dataset for detection and skips the tokenization step.
        """
        if use_tokenized_dataset:
            self.tokenized_dataset = self.io_handler.load_pickled_dataset()
        else:
            print("Tokenizing dataset...")
            self.tokenized_dataset = self._tokenize()
            self.io_handler.save_pickled_dataset(self.tokenized_dataset)

        print(self.tokenized_dataset.head())


    def export(self):
        self.io_handler.export_labels(self.labels)


    def _tokenize(self):
        tokenized_dataset = pd.DataFrame(list(), index=self.dataset.index, columns=self.dataset.columns)
        for column in self.dataset.columns:
            tokenized_dataset[column] = self.dataset[column].apply(
                lambda cell: [word for word in re.split(r'\W', cell) if word] # remove empty strings
            )
        return tokenized_dataset

