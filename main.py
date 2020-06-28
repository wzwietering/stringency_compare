from datetime import date
import os

from download_data import download_data
from euclidean_distance import calculate_euclidean_distance
from calc_dtw import calculate_dtw_distance

if not os.path.exists("OxCGRT_latest.csv") or not os.path.exists("worldPop2020.csv"):
    download_data()

# Enter the countries to analyse below
country = "Netherlands"
min_pop = 3e5  # Minimum population size
compare_count = 5  # Top k similar countries to find
start_date = date(year=2020, month=4, day=1)  # Start of analysis period
end_date = date(year=2020, month=5, day=1)  # End of analysis period
filter_on_continent = True  # Only compare countries in the same continent

# test by bart

calculate_euclidean_distance(
    country, min_pop, compare_count, start_date, end_date, filter_on_continent
)
calculate_dtw_distance(
    country, min_pop, compare_count, start_date, end_date, filter_on_continent
)
