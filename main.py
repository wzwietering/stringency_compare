import os

from download_data import download_data
from euclidean_distance import calculate_euclidean_distance
from calc_dtw import calculate_dtw_distance

if not os.path.exists("OxCGRT_latest.csv") or os.path.exists("worldPop2020.csv"):
    download_data()

# Enter the countries to analyse below
country = "Egypt"

calculate_euclidean_distance(country)
calculate_dtw_distance(country)
