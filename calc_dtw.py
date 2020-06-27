from datetime import date

import dtw
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pycountry_convert as pc


def calculate_dtw_distance(
    focal_country,
    min_pop=3e5,
    compare_count=5,
    start_date=date(year=2020, month=4, day=1),
    end_date=date(year=2020, month=5, day=1),
):
    total_days = (end_date - start_date).days
    df_period = prepare_data(start_date, end_date)
    df_period_group = df_period.groupby("CountryName")
    country = df_period_group.get_group(focal_country)
    dtw_df = execute_dtw(df_period_group, country)

    # Filter by continent
    alpha2_name = pc.country_name_to_country_alpha2(focal_country)
    continent = pc.country_alpha2_to_continent_code(alpha2_name)
    plot_result(dtw_df, df_period_group, focal_country, continent, total_days)


def prepare_data(start_date, end_date, oxcgrt="OxCGRT_latest.csv"):
    start_int = int(start_date.strftime("%Y%m%d"))
    end_int = int(end_date.strftime("%Y%m%d"))
    df = pd.read_csv(oxcgrt)
    df_period = df.loc[(df["Date"] >= start_int) & (df["Date"] < end_int)]

    df_period.loc[:, "DateId"] = df_period["Date"] - start_int
    return df_period


def execute_dtw(df_period_group, compare_group):
    dtw_results = []
    for country in df_period_group:
        try:
            country_code = pc.country_name_to_country_alpha2(
                country[0], cn_name_format="default"
            )
        except Exception as e:
            print(country[0], "has error", e)
            continue
        try:
            continent_name = pc.country_alpha2_to_continent_code(country_code)
        except Exception as e:
            print(country[0], "has error", e)
            continue

        try:
            result = dtw.dtw(
                compare_group["StringencyIndex"], country[1]["StringencyIndex"]
            )
        except Exception as e:
            print(country[0], "has error", e)
            continue

        dtw_results.append(
            [country[0], continent_name, result.distance, result.normalizedDistance]
        )
    dtw_df = pd.DataFrame(
        data=dtw_results,
        columns=["Country", "Continent", "Distance", "Normalized_distance"],
    )
    return dtw_df


def plot_result(dtw_df, df_period_group, focal_country, continent, total_days):
    nd_sort = dtw_df.loc[dtw_df["Continent"] == continent].sort_values(
        by=["Normalized_distance"]
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.suptitle("Top-4: Dynamic Time Warping")

    time_series = np.arange(total_days)
    i = 0
    for _, row in nd_sort.iterrows():
        if i == 5:
            break
        country = row["Country"]
        linewidth = 8 if country == focal_country else 3
        plt.plot(
            time_series,
            df_period_group.get_group(country)["StringencyIndex"],
            label=country,
            linewidth=linewidth,
            alpha=1,
        )
        i += 1

    plt.ylim(top=100)
    plt.ylim(bottom=0)

    ax.set_xlabel("Days")
    ax.set_ylabel("Stringency")
    plt.legend(loc="lower left")
    plt.show()
