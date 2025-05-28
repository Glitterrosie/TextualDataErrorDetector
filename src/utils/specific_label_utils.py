import pandas as pd

from error_types import ErrorType


def no_labels(data_column: pd.Series, generic_labeled_cell_indices: pd.Index) -> pd.Series:
    return pd.Series(0, index=data_column.index, dtype=int)

def set_all_labels_to_ocr(data_column: pd.Series, generic_labeled_cell_indices: pd.Index) -> pd.Series:
    label_column = pd.Series(0, index=data_column.index, dtype=int)
    label_column.loc[generic_labeled_cell_indices] = ErrorType.OCR.value
    return label_column
