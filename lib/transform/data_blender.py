import json
import os
import re

import pandas as pd
from tqdm import tqdm

from lib.tracking_decorator import TrackingDecorator

key_figure_group = "berlin-lor-monitoring-social-urban-development"

statistic_properties = [
    "inhabitants",
    "s1_percentage_unemployed",
    "s2_percentage_long_term_unemployed",
    "s3_percentage_transfer_payments_recipients",
    "s4_percentage_transfer_payments_recipients_below_15_years",
    "d1_percentage_unemployed",
    "d2_percentage_long_term_unemployed",
    "d3_percentage_transfer_payments_recipients",
    "d4_percentage_transfer_payments_recipients_below_15_years",
    "k01_youth_unemployment",
    "k02_single_parent_households",
    "k03_old_age_poverty",
    "k04_children_with_migration_background",
    "k05_inhabitants_with_migration_background",
    "k16_foreigners",
    "k06_change_proportion_of_foreigner",
    "k17_non_eu_foreigners",
    "k07_foreign_transfer_recipients",
    "k08_urban_apartments",
    "k14_living_rooms",
    "k15_living_space",
    "k09_simple_residential_area",
    "k10_duration_of_residence_over_5_years",
    "k11_migration_volume",
    "k12_balance_of_migration",
    "k13_balance_of_migration_of_children_below_6"
]

statistics = [
    f"{key_figure_group}-2013-00",
    f"{key_figure_group}-2015-00",
    f"{key_figure_group}-2017-00",
    f"{key_figure_group}-2019-00",
    f"{key_figure_group}-2021-00"
]


@TrackingDecorator.track_time
def blend_data(source_path, results_path, clean=False, quiet=False):
    # Make results path
    os.makedirs(os.path.join(results_path), exist_ok=True)

    # Initialize statistics
    json_statistics = {}

    # Iterate over LOR area types
    for lor_area_type in ["districts", "district-regions", "planning-areas"]:

        # Iterate over statistics
        for statistics_name in tqdm(sorted(statistics), desc=f"Blend statistics for {lor_area_type}", unit="statistic"):
            year = re.search(r"\b\d{4}\b", statistics_name).group()
            half_year = re.search(r"\b\d{2}(?<!\d{4})\b", statistics_name).group()

            # Load geojson
            if lor_area_type == "districts":
                geojson = read_geojson_file(
                    os.path.join(source_path, "berlin-lor-geodata", f"berlin-lor-{lor_area_type}.geojson"))
            elif int(year) <= 2020:
                geojson = read_geojson_file(
                    os.path.join(source_path, "berlin-lor-geodata", f"berlin-lor-{lor_area_type}-until-2020.geojson"))
            elif int(year) >= 2021:
                geojson = read_geojson_file(
                    os.path.join(source_path, "berlin-lor-geodata", f"berlin-lor-{lor_area_type}-from-2021.geojson"))
            else:
                geojson = None

            # Load statistics
            csv_statistics = read_csv_file(
                os.path.join(source_path, statistics_name, f"{statistics_name}-{lor_area_type}.csv"))

            # Extend geojson
            extend(
                year=year,
                half_year=half_year,
                geojson=geojson,
                statistics_name=statistics_name,
                csv_statistics=csv_statistics,
                json_statistics=json_statistics
            )

            # Write geojson file
            write_geojson_file(
                file_path=os.path.join(results_path, statistics_name,
                                       f"{key_figure_group}-{year}-{half_year}-{lor_area_type}.geojson"),
                statistic_name=f"{key_figure_group}-{year}-{half_year}-{lor_area_type}",
                geojson_content=geojson,
                clean=clean,
                quiet=quiet
            )

    # Write json statistics file
    write_json_file(
        file_path=os.path.join(results_path, f"{key_figure_group}-statistics",
                               f"{key_figure_group}-statistics.json"),
        statistic_name=f"{key_figure_group}-statistics",
        json_content=json_statistics,
        clean=clean,
        quiet=quiet
    )


def extend(year, half_year, geojson, statistics_name, csv_statistics, json_statistics):
    """
    Extends geojson and json-statistics by statistical values
    :param year:
    :param half_year:
    :param geojson:
    :param statistics_name:
    :param csv_statistics:
    :param json_statistics:
    :return:
    """

    # Check for missing files
    if csv_statistics is None:
        print(f"✗️ No data in {statistics_name}")
        return

    # Check if file needs to be created
    for feature in sorted(geojson["features"], key=lambda feature: feature["properties"]["id"]):
        feature_id = feature["properties"]["id"]

        # Filter statistics
        statistic_filtered = csv_statistics[csv_statistics["id"].astype(str).str.startswith(feature_id)]

        # Check for missing data
        if statistic_filtered.shape[0] == 0 or \
                int(statistic_filtered["id"].sum()) == 0:
            print(f"✗️ No data in {statistics_name} for id={feature_id}")
            continue

        # Blend data
        blend_data_into_feature(feature, statistic_filtered)
        blend_data_into_json(year, half_year, feature_id, feature, json_statistics)


def blend_data_into_feature(feature, statistics):
    # Add new properties
    for property_name in statistic_properties:
        add_property(feature, statistics, property_name)

    return feature


def blend_data_into_json(year, half_year, feature_id, feature, json_statistics):
    # Build structure
    if year not in json_statistics:
        json_statistics[year] = {}
    if half_year not in json_statistics[year]:
        json_statistics[year][half_year] = {}

    # Add properties
    json_statistics[year][half_year][feature_id] = feature["properties"]


def add_property(feature, statistics, property_name):
    if statistics is not None and property_name in statistics:
        try:
            feature["properties"][f"{property_name}"] = float(statistics[property_name].sum())
        except ValueError:
            feature["properties"][f"{property_name}"] = 0
        except TypeError:
            feature["properties"][f"{property_name}"] = 0


def load_population_statistics(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as json_file:
        return json.load(json_file, strict=False)


def get_inhabitants(population_statistics, year, feature_id):
    try:
        return population_statistics[year]["02"][feature_id]["inhabitants"]
    except KeyError:
        # print(f"✗️ No population data for id={feature_id}")
        return None


def read_csv_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as csv_file:
            return pd.read_csv(csv_file, dtype={"id": "str"})
    else:
        return None


def read_geojson_file(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as geojson_file:
        return json.load(geojson_file, strict=False)


def write_geojson_file(file_path, statistic_name, geojson_content, clean, quiet):
    if not os.path.exists(file_path) or clean:

        # Make results path
        path_name = os.path.dirname(file_path)
        os.makedirs(os.path.join(path_name), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as geojson_file:
            json.dump(geojson_content, geojson_file, ensure_ascii=False)

            if not quiet:
                print(f"✓ Blend data from {statistic_name} into {os.path.basename(file_path)}")
    else:
        print(f"✓ Already exists {os.path.basename(file_path)}")


def write_json_file(file_path, statistic_name, json_content, clean, quiet):
    if not os.path.exists(file_path) or clean:

        # Make results path
        path_name = os.path.dirname(file_path)
        os.makedirs(os.path.join(path_name), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(json_content, json_file, ensure_ascii=False)

            if not quiet:
                print(f"✓ Aggregate data from {statistic_name} into {os.path.basename(file_path)}")
    else:
        print(f"✓ Already exists {os.path.basename(file_path)}")
