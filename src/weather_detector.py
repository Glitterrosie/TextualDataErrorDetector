from detector import Detector


class WeatherDetector(Detector):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)

    def detect(self, use_tokenized_dataset: bool = False):
        print(f"--- Australian Weather Dataset ---")
        print(f"Number of cells: {self.dataset.size}, Number of rows: {self.dataset.shape[0]}")

        super().detect(use_tokenized_dataset)
