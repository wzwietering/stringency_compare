from _collections import defaultdict
from datetime import date
import csv

import matplotlib.pyplot as plt
import numpy as np
import pycountry_convert as pc


def calculate_euclidean_distance(
    focal_country,
    min_pop=3e5,
    compare_count=5,
    start_date=date(year=2020, month=4, day=1),
    end_date=date(year=2020, month=5, day=1),
    filter_on_continent=True,
):
    total_days = (end_date - start_date).days
    # Load data
    stringency_records, population_records = prepare_data()

    # Filter on time range
    stringency_records = list(
        filter(
            lambda record: within_timerange(record, start_date, end_date),
            stringency_records,
        )
    )

    # Setup country datastructures
    countries, country2i, i2country = prepare_countries(stringency_records)

    # Create stringency matrix
    stringency_timeseries = create_stringecy_matrix(
        stringency_records, i2country, total_days
    )

    # Calculate 1D Euclidean distance
    euclidean_distance_srt = one_d_euclidean_distance(
        stringency_timeseries, country2i, countries, focal_country, total_days
    )

    # Filter on population size
    euclidean_distance_srt = list(
        filter(
            lambda country: filter_small_countries(
                country, population_records, min_pop
            ),
            euclidean_distance_srt,
        )
    )

    if filter_on_continent:
        alpha2_name = pc.country_name_to_country_alpha2(focal_country)
        continent = pc.country_alpha2_to_continent_code(alpha2_name)
        # Filter on continent
        euclidean_distance_srt = list(
            filter(
                lambda country: filter_continent(country, continent),
                euclidean_distance_srt,
            )
        )

    # Plot the result
    plot_result(
        euclidean_distance_srt,
        stringency_timeseries,
        total_days,
        compare_count,
        country2i,
        focal_country,
    )


def prepare_data(oxcgrt="OxCGRT_latest.csv", worldpop="worldPop2020.csv"):
    stringency_records = []
    population_records = []

    with open("OxCGRT_latest.csv") as file:
        for row in csv.DictReader(file, skipinitialspace=True):
            stringency_records.append(row)

    with open("worldPop2020.csv") as file:
        for row in csv.DictReader(file, skipinitialspace=True):
            population_records.append(row)
    return stringency_records, population_records


def within_timerange(record, start_date, end_date):
    d = record["Date"]
    r_date = date(year=int(d[0:4]), month=int(d[4:6]), day=int(d[6:8]))
    return r_date >= start_date and r_date < end_date


def prepare_countries(stringency_records):
    countries = []
    for r in stringency_records:
        if r["CountryName"] not in countries:
            countries.append(r["CountryName"])

    country2i = defaultdict(lambda: len(country2i))
    i2country = dict()
    for country in countries:
        i2country[country2i[country]] = country
    return countries, country2i, i2country


def create_stringecy_matrix(stringency_records, i2country, total_days):
    stringency_timeseries = np.empty((len(i2country), total_days))

    countries = []
    country = 0
    day = 0
    countries.append(stringency_records[0]["CountryName"])
    countries_to_exclude = []

    for r in stringency_records:

        if r["CountryName"] not in countries:
            day = 0
            country += 1
            countries.append(r["CountryName"])

        stringency = r["StringencyIndex"]
        try:
            float(stringency)
        except ValueError:
            c = i2country[country]
            if c not in countries_to_exclude:
                countries_to_exclude.append(c)
            continue

        stringency_timeseries[country, day] = stringency
        day += 1
    return stringency_timeseries


def one_d_euclidean_distance(
    stringency_timeseries, country2i, countries, focal_country, total_days, sort=True
):
    euclidean_distance = []
    for country in countries:
        variance = 0
        for day in range(total_days):
            distance = (
                stringency_timeseries[country2i[country], day]
                - stringency_timeseries[country2i[focal_country], day]
            )
            distance_abs = abs(distance)
            variance += distance_abs

        euclidean_averaged = variance / total_days
        euclidean_distance.append({"country": country, "distance": euclidean_averaged})

    if sort:
        euclidean_distance_srt = sorted(
            euclidean_distance, key=lambda key: key["distance"]
        )
        return euclidean_distance_srt
    return euclidean_distance


def filter_small_countries(c, population_records, min_pop):
    population = 0
    for record in population_records:
        if c["country"] == record["name"]:
            population = float(record["pop2020"]) * 1000
            if population > min_pop:
                return True
            else:
                return False

    return False


def filter_continent(c, filter_continent_name="EU"):
    country_code = pc.country_name_to_country_alpha2(
        c["country"], cn_name_format="default"
    )
    try:
        continent_name = pc.country_alpha2_to_continent_code(country_code)
    except Exception as e:
        print(country_code, "has error", e)
        return False
    if continent_name == filter_continent_name:
        return True
    else:
        return False


def plot_result(
    euclidean_distance_srt,
    stringency_timeseries,
    total_days,
    compare_count,
    country2i,
    focal_country,
):
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.suptitle("Top-4: One-dimensional Euclidean Distance")

    time_series = np.arange(total_days)
    for i in range(compare_count):
        country = euclidean_distance_srt[i]["country"]
        linewidth = 8 if country == focal_country else 3
        plt.plot(
            time_series,
            stringency_timeseries[country2i[country]],
            label=country,
            linewidth=linewidth,
            alpha=1,
        )

    plt.ylim(top=100)
    plt.ylim(bottom=0)

    ax.set_xlabel("Days")
    ax.set_ylabel("Stringency")
    plt.legend(loc="lower left")
    plt.show()
