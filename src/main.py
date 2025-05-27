from imdb_detector import IMDBDetector
from medical_detector import MedicalDetector
from weather_detector import WeatherDetector


def main():
    use_tokenized_dataset = False # setting this to false will tokenize the dataset and save it as a pickle file

    imdb_detector = IMDBDetector("../datasets/imdb_subset1_group1_w_errors.csv")
    imdb_detector.detect(use_tokenized_dataset)
    imdb_detector.export()

    weather_detector = WeatherDetector("../datasets/weather_subset1_group1_w_errors.csv")
    weather_detector.detect(use_tokenized_dataset)
    weather_detector.export()

    medical_detector = MedicalDetector("../datasets/medical_subset1_group1_w_errors.csv")
    medical_detector.detect(use_tokenized_dataset)
    medical_detector.export()

if __name__ == "__main__":
    main()
