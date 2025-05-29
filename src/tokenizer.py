import pandas as pd
import re

class Tokenizer():
    def tokenize_dataset(self, dataset):
        tokenized_dataset = pd.DataFrame(list(), index=dataset.index, columns=dataset.columns)
        for column in dataset.columns:
            tokenized_dataset[column] = dataset[column].apply(
                lambda cell: [word for word in re.split(r'\W', cell) if word] # remove empty strings
            )
        return tokenized_dataset
    
    def tokenize_column(self, one_column_data: pd.Series) -> pd.Series:
        return one_column_data.apply(
            lambda cell: [word for word in re.split(r'\W+', str(cell)) if word]
        )
    
    def tokenize_cell(self, cell_value: str) -> str:
        return re.split(r'\W+', str(cell_value))
