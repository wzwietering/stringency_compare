import os

from download_data import download_data
from euclidean_distance import calculate_euclidean_distance
from calc_dtw import calculate_dtw_distance

if not os.path.exists("OxCGRT_latest.csv") or not os.path.exists("worldPop2020.csv"):
    download_data()

# Enter the countries to analyse below
country = "Netherlands"
filter_on_continent = True

calculate_euclidean_distance(country, filter_on_continent=filter_on_continent)
calculate_dtw_distance(country, filter_on_continent=filter_on_continent)
