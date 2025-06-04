import re

import pandas as pd

REGEX = r'\W+'

class Tokenizer():
    def tokenize_dataset(self, dataset: pd.DataFrame) -> pd.DataFrame:
        tokenized_dataset = pd.DataFrame(list(), index=dataset.index, columns=dataset.columns)
        for column in dataset.columns:
            tokenized_dataset[column] = dataset[column].apply(
                lambda cell: self.tokenize_cell(cell)
            )
        return tokenized_dataset
    
    def tokenize_column(self, one_column_data: pd.Series) -> pd.Series:
        return one_column_data.apply(
            lambda cell: self.tokenize_cell(cell)
        )
    
    def tokenize_cell(self, cell_value: str) -> list:
        all_tokens = re.split(REGEX, str(cell_value))
        non_empty_tokens = [token for token in all_tokens if token]
        return non_empty_tokens
