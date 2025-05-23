from imdb_detector import IMDBDetector
from medical_detector import MedicalDetector
from weather_detector import WeatherDetector


def main():
    imdb_detector = IMDBDetector("../datasets/imdb_subset1_group1_w_errors.csv")
    imdb_detector.detect()
    imdb_detector.export()

    weather_detector = WeatherDetector("../datasets/weather_subset1_group1_w_errors.csv")
    weather_detector.detect()
    weather_detector.export()

    medical_detector = MedicalDetector("../datasets/medical_subset1_group1_w_errors.csv")
    medical_detector.detect()
    medical_detector.export()

if __name__ == "__main__":
    main()
