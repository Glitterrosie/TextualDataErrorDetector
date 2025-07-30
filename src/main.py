import time
from imdb_detector import IMDBDetector
from medical_detector import MedicalDetector
from weather_detector import WeatherDetector


def main():
    start_time = time.time()

    imdb_detector = IMDBDetector("../datasets/imdb_subset1_group1_w_errors.csv")
    imdb_detector.detect()
    imdb_detector.export()

    weather_detector = WeatherDetector("../datasets/weather_subset1_group1_w_errors.csv")
    weather_detector.detect()
    weather_detector.export()

    medical_detector = MedicalDetector("../datasets/medical_subset1_group1_w_errors.csv")
    medical_detector.detect()
    medical_detector.export()

    end_time = time.time()
    print(f"Time taken for all datasets: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
