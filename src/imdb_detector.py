from detector import Detector


class IMDBDetector(Detector):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)

    def detect(self):
        print(f"--- IMDB Dataset ---")
        print(f"Number of cells: {self.dataset.size}, Number of rows: {self.dataset.shape[0]}")

        super().detect() 

        number_columns = ["cast_id", "cast_person_id", "cast_movie_id", "cast_nr_order", "cast_role_id", "person_id", "person_info_type_id", "title_id", "kind_id", "production_year", "episode_of_id", "season_nr", "episode_nr", "series_years"]
        self.check_for_ocr(number_columns) #2.07%
        print("Finished OCR")
        self.check_for_typo_vectorized() #3.31%
        print("Finished Typo")
        self.check_for_misspellings_short()
        print("Finished Misspellings")

    def get_column_generic_label_mapping(self):
        pass

    def get_column_specific_label_mapping(self):
        pass

