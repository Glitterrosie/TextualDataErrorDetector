from detector import Detector


class IMDBDetector(Detector):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)

    def detect(self, use_tokenized_dataset: bool = False):
        print(f"--- IMDB Dataset ---")
        print(f"Number of cells: {self.dataset.size}, Number of rows: {self.dataset.shape[0]}")

        super().detect(use_tokenized_dataset) 

        number_columns = ["cast_id", "cast_person_id", "cast_movie_id", "cast_nr_order", "cast_role_id", "person_id", "person_info_type_id", "title_id", "kind_id", "production_year", "episode_of_id", "season_nr", "episode_nr", "series_years"]
        self.check_for_ocr(number_columns) #2.07%
        self.check_for_typo() #3.31%
        self.check_for_misspellings()
