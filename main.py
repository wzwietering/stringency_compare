import os

from download_data import download_data
from euclidean_distance import calculate_euclidean_distance
from calc_dtw import calculate_dtw_distance

if not os.path.exists("OxCGRT_latest.csv") or os.path.exists("worldPop202.csv"):
    download_data()

# Enter the countries to analyse below
africa_country = "Egypt"
asia_country = "Brunei"
europe_country = "Netherlands"
north_america_country = "Canada"
oceania_country = "Australia"
south_america_country = "Ecuador"

calculate_euclidean_distance(asia_country)
calculate_dtw_distance(asia_country)
