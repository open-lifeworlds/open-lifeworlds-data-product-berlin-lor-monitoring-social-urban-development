import copy
import json
import os
import statistics as stats

import pandas as pd

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

pre_2020_statistics = [
    ["berlin-lor-monitoring-social-urban-development-2013-00",
     "berlin-lor-monitoring-social-urban-development-2013-00"],
    ["berlin-lor-monitoring-social-urban-development-2015-00",
     "berlin-lor-monitoring-social-urban-development-2015-00"],
    ["berlin-lor-monitoring-social-urban-development-2017-00",
     "berlin-lor-monitoring-social-urban-development-2017-00"],
    ["berlin-lor-monitoring-social-urban-development-2019-00", "berlin-lor-monitoring-social-urban-development-2019-00"]
]
post_2020_statistics = [
    ["berlin-lor-monitoring-social-urban-development-2021-00", "berlin-lor-monitoring-social-urban-development-2021-00"]
]


@TrackingDecorator.track_time
def blend_data(source_path, results_path, clean=False, quiet=False):
    # Make results path
    os.makedirs(os.path.join(results_path), exist_ok=True)

    source_geodata_path = os.path.join(source_path, "berlin-lor-geodata")

    # Statistics
    statistics_lor_districts = {}
    statistics_lor_district_regions = {}
    statistics_lor_planning_areas = {}

    # Load geojson
    geojson_lor_districts = read_geojson_file(os.path.join(source_geodata_path, "berlin-lor-districts.geojson"))
    geojson_lor_district_regions = read_geojson_file(
        os.path.join(source_geodata_path, "berlin-lor-district-regions-until-2020.geojson"))
    geojson_lor_planning_areas = read_geojson_file(
        os.path.join(source_geodata_path, "berlin-lor-planning-areas-until-2020.geojson"))

    # Iterate over statistics
    for statistic_path, statistic_name in pre_2020_statistics:
        year = statistic_name.split(sep="-")[6]
        half_year = statistic_name.split(sep="-")[7]

        # Load statistics
        statistic_1 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-1.csv"))
        statistic_2_1 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-2-1.csv"))
        statistic_2_2 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-2-2.csv"))
        statistic_2_3 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-2-3.csv"))
        statistic_3 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-3.csv"))
        statistic_4_1 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-4-1.csv"))
        statistic_4_2 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-4-2.csv"))
        statistic_4_3 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-4-3.csv"))

        # Extend districts
        geojson_lor_districts_extended, statistics_lor_districts = extend_districts(
            statistics=statistics_lor_districts,
            year=year,
            half_year=half_year,
            statistic_name=statistic_name,
            statistic_2_3=statistic_2_3,
            statistic_4_3=statistic_4_3,
            geojson=geojson_lor_districts
        )

        # Extend district regions
        geojson_lor_district_regions_extended, statistics_lor_district_regions = extend_district_regions(
            statistics=statistics_lor_district_regions,
            year=year,
            half_year=half_year,
            statistic_name=statistic_name,
            statistic_2_2=statistic_2_2,
            statistic_4_2=statistic_4_2,
            geojson=geojson_lor_district_regions
        )

        # Extend planning areas
        geojson_lor_planning_areas_extended, statistics_lor_planning_areas = extend_planning_areas(
            statistics=statistics_lor_planning_areas,
            year=year,
            half_year=half_year,
            statistic_name=statistic_name,
            statistic_1=statistic_1,
            statistic_2_1=statistic_2_1,
            statistic_3=statistic_3,
            statistic_4_1=statistic_4_1,
            geojson=geojson_lor_planning_areas
        )

        # Write geojson files
        write_geojson_file(
            file_path=os.path.join(results_path, statistic_path,
                                   f"{key_figure_group}-{year}-{half_year}-districts.geojson"),
            statistic_name=f"{key_figure_group}-{year}-{half_year}-districts",
            geojson_content=geojson_lor_districts_extended,
            clean=clean,
            quiet=quiet
        )
        write_geojson_file(
            file_path=os.path.join(results_path, statistic_path,
                                   f"{key_figure_group}-{year}-{half_year}-district-regions.geojson"),
            statistic_name=f"{key_figure_group}-{year}-{half_year}-district-regions",
            geojson_content=geojson_lor_district_regions_extended,
            clean=clean,
            quiet=quiet
        )
        write_geojson_file(
            file_path=os.path.join(results_path, statistic_path,
                                   f"{key_figure_group}-{year}-{half_year}-planning-areas.geojson"),
            statistic_name=f"{key_figure_group}-{year}-{half_year}-planning-areas",
            geojson_content=geojson_lor_planning_areas_extended,
            clean=clean,
            quiet=quiet
        )

    # Load geojson
    geojson_lor_districts = read_geojson_file(os.path.join(source_geodata_path, "berlin-lor-districts.geojson"))
    geojson_lor_district_regions = read_geojson_file(
        os.path.join(source_geodata_path, "berlin-lor-district-regions-from-2021.geojson"))
    geojson_lor_planning_areas = read_geojson_file(
        os.path.join(source_geodata_path, "berlin-lor-planning-areas-from-2021.geojson"))

    # Iterate over statistics
    for statistic_path, statistic_name in post_2020_statistics:
        year = statistic_name.split(sep="-")[6]
        half_year = statistic_name.split(sep="-")[7]

        # Load statistics
        statistic_1 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-1.csv"))
        statistic_2_1 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-2-1.csv"))
        statistic_2_2 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-2-2.csv"))
        statistic_2_3 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-2-3.csv"))
        statistic_3 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-3.csv"))
        statistic_4_1 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-4-1.csv"))
        statistic_4_2 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-4-2.csv"))
        statistic_4_3 = read_csv_file(os.path.join(source_path, statistic_path, f"{statistic_name}-4-3.csv"))

        # Extend districts
        geojson_lor_districts_extended, statistics_lor_planning_areas = extend_districts_post_2020(
            statistics=statistics_lor_planning_areas,
            year=year,
            half_year=half_year,
            statistic_name=statistic_name,
            statistic_2_3=statistic_2_3,
            statistic_4_3=statistic_4_3,
            geojson=geojson_lor_districts
        )

        # Extend district regions
        geojson_lor_district_regions_extended, statistics_lor_planning_areas = extend_district_regions_post_2020(
            statistics=statistics_lor_planning_areas,
            year=year,
            half_year=half_year,
            statistic_name=statistic_name,
            statistic_2_2=statistic_2_2,
            statistic_4_2=statistic_4_2,
            geojson=geojson_lor_district_regions
        )

        # Extend planning areas
        geojson_lor_planning_areas_extended, statistics_lor_planning_areas = extend_planning_areas_post_2020(
            statistics=statistics_lor_planning_areas,
            year=year,
            half_year=half_year,
            statistic_name=statistic_name,
            statistic_1=statistic_1,
            statistic_2_1=statistic_2_1,
            statistic_3=statistic_3,
            statistic_4_1=statistic_4_1,
            geojson=geojson_lor_planning_areas
        )

        # Write geojson files
        write_geojson_file(
            file_path=os.path.join(results_path, statistic_path,
                                   f"{key_figure_group}-{year}-{half_year}-districts.geojson"),
            statistic_name=f"{key_figure_group}-{year}-{half_year}-districts",
            geojson_content=geojson_lor_districts_extended,
            clean=clean,
            quiet=quiet
        )
        write_geojson_file(
            file_path=os.path.join(results_path, statistic_path,
                                   f"{key_figure_group}-{year}-{half_year}-district-regions.geojson"),
            statistic_name=f"{key_figure_group}-{year}-{half_year}-district-regions",
            geojson_content=geojson_lor_district_regions_extended,
            clean=clean,
            quiet=quiet
        )
        write_geojson_file(
            file_path=os.path.join(results_path, statistic_path,
                                   f"{key_figure_group}-{year}-{half_year}-planning-areas.geojson"),
            statistic_name=f"{key_figure_group}-{year}-{half_year}-planning-areas",
            geojson_content=geojson_lor_planning_areas_extended,
            clean=clean,
            quiet=quiet
        )

    # Write json file
    write_json_file(
        file_path=os.path.join(results_path, f"{key_figure_group}-statistics",
                               f"{key_figure_group}-districts-statistics.json"),
        statistic_name=f"{key_figure_group}-districts-statistics",
        json_content=statistics_lor_districts,
        clean=clean,
        quiet=quiet
    )
    write_json_file(
        file_path=os.path.join(results_path, f"{key_figure_group}-statistics",
                               f"{key_figure_group}-district-regions-statistics.json"),
        statistic_name=f"{key_figure_group}-district-regions-statistics",
        json_content=statistics_lor_district_regions,
        clean=clean,
        quiet=quiet
    )
    write_json_file(
        file_path=os.path.join(results_path, f"{key_figure_group}-statistics",
                               f"{key_figure_group}-planning-areas-statistics.json"),
        statistic_name=f"{key_figure_group}-planning-areas-statistics",
        json_content=statistics_lor_planning_areas,
        clean=clean,
        quiet=quiet
    )


def read_csv_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as csv_file:
            return pd.read_csv(csv_file)
    else:
        return None


def read_geojson_file(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as geojson_file:
        return json.load(geojson_file, strict=False)


def write_geojson_file(file_path, statistic_name, geojson_content, clean, quiet):
    if not os.path.exists(file_path) or clean:
        file_name = os.path.basename(file_path)

        with open(file_path, "w", encoding="utf-8") as geojson_file:
            json.dump(geojson_content, geojson_file, ensure_ascii=False)

            if not quiet:
                print(f"✓ Blend data from {statistic_name} into {file_name}")


def write_json_file(file_path, statistic_name, json_content, clean, quiet):
    if not os.path.exists(file_path) or clean:
        path_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)

        os.makedirs(os.path.join(path_name), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(json_content, json_file, ensure_ascii=False)

            if not quiet:
                print(f"✓ Aggregate data from {statistic_name} into {file_name}")


def extend_districts(statistics, year, half_year,
                     statistic_name, statistic_2_3, statistic_4_3,
                     geojson):
    geojson_extended = copy.deepcopy(geojson)

    # Check for missing files
    if statistic_2_3 is None:
        print(f"✗️ No district data in {statistic_name}")
    if statistic_4_3 is None:
        print(f"✗️ No district data in {statistic_name}")

    # Check if file needs to be created
    for feature in geojson_extended["features"]:
        feature_id = feature["properties"]["id"]
        area_sqm = feature["properties"]["area"]
        area_sqkm = area_sqm / 1_000_000

        # Filter statistics
        statistic_2_3_filtered = statistic_2_3.loc[
            (statistic_2_3["id"] == int(feature_id))] if statistic_2_3 is not None else None
        statistic_4_3_filtered = statistic_4_3.loc[
            (statistic_4_3["id"] == int(feature_id))] if statistic_4_3 is not None else None

        # Check for missing data
        if statistic_2_3_filtered is not None and statistic_2_3_filtered.shape[0] == 0:
            print(f"✗️ No district data in {statistic_name} for id={feature_id}")
        if statistic_4_3_filtered is not None and statistic_4_3_filtered.shape[0] == 0:
            print(f"✗️ No district data in {statistic_name} for id={feature_id}")

        # Blend data
        feature = blend_district_data(
            feature=feature, area_sqkm=area_sqkm,
            statistic_2_3_filtered=statistic_2_3_filtered,
            statistic_4_3_filtered=statistic_4_3_filtered
        )

        # Build structure
        if year not in statistics:
            statistics[year] = {}
        if half_year not in statistics[year]:
            statistics[year][half_year] = {}

        # Add properties
        statistics[year][half_year][feature_id] = feature["properties"]

    # Calculate average and median values
    for year, half_years in statistics.items():
        for half_year, feature_ids in half_years.items():
            values = {}

            for feature_id, properties in feature_ids.items():
                for property_name, property_value in properties.items():
                    if property_name in statistic_properties:
                        if property_name not in values:
                            values[property_name] = []
                        values[property_name].append(property_value)

            statistics[year][half_year]["average"] = {key: stats.mean(lst) for key, lst in values.items()}
            statistics[year][half_year]["median"] = {key: stats.median(lst) for key, lst in values.items()}

    return geojson_extended, statistics


def extend_district_regions(statistics, year, half_year,
                            statistic_name, statistic_2_2, statistic_4_2,
                            geojson):
    geojson_extended = copy.deepcopy(geojson)

    # Check for missing files
    if statistic_2_2 is None:
        print(f"✗️ No district region data in {statistic_name}-2-2")
    if statistic_4_2 is None:
        print(f"✗️ No district region data in {statistic_name}-4-2")

    # Check if file needs to be created
    for feature in geojson_extended["features"]:
        feature_id = feature["properties"]["id"]
        area_sqm = feature["properties"]["area"]
        area_sqkm = area_sqm / 1_000_000

        # Filter statistics
        statistic_2_2_filtered = statistic_2_2.loc[
            (statistic_2_2["id"] == int(feature_id))] if statistic_2_2 is not None else None
        statistic_4_2_filtered = statistic_4_2.loc[
            (statistic_4_2["id"] == int(feature_id))] if statistic_4_2 is not None else None

        # Check for missing data
        if statistic_2_2_filtered is not None and statistic_2_2_filtered.shape[0] == 0:
            print(f"✗️ No district region data in {statistic_name}-2-2 for id={feature_id}")
        if statistic_4_2_filtered is not None and statistic_4_2_filtered.shape[0] == 0:
            print(f"✗️ No district region data in {statistic_name}-4-2 for id={feature_id}")

        # Blend data
        feature = blend_district_region_data(
            feature=feature, area_sqkm=area_sqkm,
            statistic_2_2_filtered=statistic_2_2_filtered,
            statistic_4_2_filtered=statistic_4_2_filtered
        )

        # Build structure
        if year not in statistics:
            statistics[year] = {}
        if half_year not in statistics[year]:
            statistics[year][half_year] = {}

        # Add properties
        statistics[year][half_year][feature_id] = feature["properties"]

    # Calculate average and median values
    for year, half_years in statistics.items():
        for half_year, feature_ids in half_years.items():
            values = {}

            for feature_id, properties in feature_ids.items():
                for property_name, property_value in properties.items():
                    if property_name in statistic_properties:
                        if property_name not in values:
                            values[property_name] = []
                        values[property_name].append(property_value)

            statistics[year][half_year]["average"] = {key: stats.mean(lst) for key, lst in values.items()}
            statistics[year][half_year]["median"] = {key: stats.median(lst) for key, lst in values.items()}

    return geojson_extended, statistics


def extend_planning_areas(statistics, year, half_year,
                          statistic_name, statistic_1, statistic_2_1, statistic_3, statistic_4_1,
                          geojson):
    geojson_extended = copy.deepcopy(geojson)

    # Check for missing files
    if statistic_1 is None:
        print(f"✗️ No planning area data in {statistic_name}-1")
    if statistic_2_1 is None:
        print(f"✗️ No planning area data in {statistic_name}-2-2")
    if statistic_3 is None:
        print(f"✗️ No planning area data in {statistic_name}-3")
    if statistic_4_1 is None:
        print(f"✗️ No planning area data in {statistic_name}-4-1")

    # Check if file needs to be created
    for feature in geojson_extended["features"]:
        feature_id = feature["properties"]["id"]
        area_sqm = feature["properties"]["area"]
        area_sqkm = area_sqm / 1_000_000

        # Filter statistics
        statistic_1_filtered = statistic_1.loc[
            (statistic_1["id"] == int(feature_id))] if statistic_1 is not None else None
        statistic_2_1_filtered = statistic_2_1.loc[
            (statistic_2_1["id"] == int(feature_id))] if statistic_2_1 is not None else None
        statistic_3_filtered = statistic_3.loc[
            (statistic_3["id"] == int(feature_id))] if statistic_3 is not None else None
        statistic_4_1_filtered = statistic_4_1.loc[
            (statistic_4_1["id"] == int(feature_id))] if statistic_4_1 is not None else None

        # Check for missing data
        if statistic_1_filtered is not None and statistic_1_filtered.shape[0] == 0:
            print(f"✗️ No planning area data in {statistic_name}-1 for id={feature_id}")
        if statistic_2_1_filtered is not None and statistic_2_1_filtered.shape[0] == 0:
            print(f"✗️ No planning area data in {statistic_name}-2-2 for id={feature_id}")
        if statistic_3_filtered is not None and statistic_3_filtered.shape[0] == 0:
            print(f"✗️ No planning area data in {statistic_name}-3 for id={feature_id}")
        if statistic_4_1_filtered is not None and statistic_4_1_filtered.shape[0] == 0:
            print(f"✗️ No planning area data in {statistic_name}-4-1 for id={feature_id}")

        # Blend data
        feature = blend_planning_area_data(
            feature=feature, area_sqkm=area_sqkm,
            statistic_1_filtered=statistic_1_filtered,
            statistic_2_1_filtered=statistic_2_1_filtered,
            statistic_3_filtered=statistic_3_filtered,
            statistic_4_1_filtered=statistic_4_1_filtered
        )

        # Build structure
        if year not in statistics:
            statistics[year] = {}
        if half_year not in statistics[year]:
            statistics[year][half_year] = {}

        # Add properties
        statistics[year][half_year][feature_id] = feature["properties"]

    # Calculate average and median values
    for year, half_years in statistics.items():
        for half_year, feature_ids in half_years.items():
            values = {}

            for feature_id, properties in feature_ids.items():
                for property_name, property_value in properties.items():
                    if property_name in statistic_properties:
                        if property_name not in values:
                            values[property_name] = []
                        values[property_name].append(property_value)

            statistics[year][half_year]["average"] = {key: stats.mean(lst) for key, lst in values.items()}
            statistics[year][half_year]["median"] = {key: stats.median(lst) for key, lst in values.items()}

    return geojson_extended, statistics


def extend_districts_post_2020(statistics, year, half_year, statistic_name, statistic_2_3, statistic_4_3, geojson):
    geojson_extended = copy.deepcopy(geojson)

    # Check for missing files
    if statistic_2_3 is None:
        print(f"✗️ No district data in {statistic_name}-2-3")
    if statistic_4_3 is None:
        print(f"✗️ No district data in {statistic_name}-4-3")

    # Check if file needs to be created
    for feature in geojson_extended["features"]:
        feature_id = feature["properties"]["id"]
        area_sqm = feature["properties"]["area"]
        area_sqkm = area_sqm / 1_000_000

        # Filter statistics
        statistic_2_3_filtered = statistic_2_3.loc[
            (statistic_2_3["id"] == int(feature_id))] if statistic_2_3 is not None else None
        statistic_4_3_filtered = statistic_4_3.loc[
            (statistic_4_3["id"] == int(feature_id))] if statistic_4_3 is not None else None

        # Check for missing data
        if statistic_2_3_filtered is not None and statistic_2_3_filtered.shape[0] == 0:
            print(f"✗️ No district data in {statistic_name}-2-3 for id={feature_id}")
        if statistic_4_3_filtered is not None and statistic_4_3_filtered.shape[0] == 0:
            print(f"✗️ No district data in {statistic_name}-4-3 for id={feature_id}")

        # Blend data
        feature = blend_district_data(
            feature=feature, area_sqkm=area_sqkm,
            statistic_2_3_filtered=statistic_2_3_filtered,
            statistic_4_3_filtered=statistic_4_3_filtered
        )

        # Build structure
        if year not in statistics:
            statistics[year] = {}
        if half_year not in statistics[year]:
            statistics[year][half_year] = {}

        # Add properties
        statistics[year][half_year][feature_id] = feature["properties"]

    # Calculate average and median values
    for year, half_years in statistics.items():
        for half_year, feature_ids in half_years.items():
            values = {}

            for feature_id, properties in feature_ids.items():
                for property_name, property_value in properties.items():
                    if property_name in statistic_properties:
                        if property_name not in values:
                            values[property_name] = []
                        values[property_name].append(property_value)

            statistics[year][half_year]["average"] = {key: stats.mean(lst) for key, lst in values.items()}
            statistics[year][half_year]["median"] = {key: stats.median(lst) for key, lst in values.items()}

    return geojson_extended, statistics


def extend_district_regions_post_2020(statistics, year, half_year,
                                      statistic_name, statistic_2_2, statistic_4_2,
                                      geojson):
    geojson_extended = copy.deepcopy(geojson)

    # Check for missing files
    if statistic_2_2 is None:
        print(f"✗️ No district region data in {statistic_name}-4-2-2")
    if statistic_4_2 is None:
        print(f"✗️ No district region data in {statistic_name}-4-2")

    # Check if file needs to be created
    for feature in geojson_extended["features"]:
        feature_id = feature["properties"]["id"]
        area_sqm = feature["properties"]["area"]
        area_sqkm = area_sqm / 1_000_000

        # Filter statistics
        statistic_2_2_filtered = statistic_2_2.loc[
            (statistic_2_2["id"] == int(feature_id))] if statistic_2_2 is not None else None
        statistic_4_2_filtered = statistic_4_2.loc[
            (statistic_4_2["id"] == int(feature_id))] if statistic_4_2 is not None else None

        # Check for missing data
        if statistic_2_2_filtered is not None and statistic_2_2_filtered.shape[0] == 0:
            print(f"✗️ No district region data in {statistic_name}-4-2-2 for id={feature_id}")
        if statistic_4_2_filtered is not None and statistic_4_2_filtered.shape[0] == 0:
            print(f"✗️ No district region data in {statistic_name}-4-2 for id={feature_id}")

        # Blend data
        feature = blend_district_region_data_post_2020(
            feature=feature, area_sqkm=area_sqkm,
            statistic_2_2_filtered=statistic_2_2_filtered,
            statistic_4_2_filtered=statistic_4_2_filtered
        )

        # Build structure
        if year not in statistics:
            statistics[year] = {}
        if half_year not in statistics[year]:
            statistics[year][half_year] = {}

        # Add properties
        statistics[year][half_year][feature_id] = feature["properties"]

    # Calculate average and median values
    for year, half_years in statistics.items():
        for half_year, feature_ids in half_years.items():
            values = {}

            for feature_id, properties in feature_ids.items():
                for property_name, property_value in properties.items():
                    if property_name in statistic_properties:
                        if property_name not in values:
                            values[property_name] = []
                        values[property_name].append(property_value)

            statistics[year][half_year]["average"] = {key: stats.mean(lst) for key, lst in values.items()}
            statistics[year][half_year]["median"] = {key: stats.median(lst) for key, lst in values.items()}

    return geojson_extended, statistics


def extend_planning_areas_post_2020(statistics, year, half_year,
                                    statistic_name, statistic_1, statistic_2_1, statistic_3, statistic_4_1,
                                    geojson):
    geojson_extended = copy.deepcopy(geojson)

    # Check for missing files
    if statistic_1 is None:
        print(f"✗️ No planning area data in {statistic_name}-1")
    if statistic_2_1 is None:
        print(f"✗️ No planning area data in {statistic_name}-2-1")
    if statistic_3 is None:
        print(f"✗️ No planning area data in {statistic_name}-3")
    if statistic_4_1 is None:
        print(f"✗️ No planning area data in {statistic_name}-4-1")

    for feature in geojson_extended["features"]:
        feature_id = feature["properties"]["id"]
        area_sqm = feature["properties"]["area"]
        area_sqkm = area_sqm / 1_000_000

        # Filter statistics
        statistic_1_filtered = statistic_1.loc[
            (statistic_1["id"] == int(feature_id))] if statistic_1 is not None else None
        statistic_2_1_filtered = statistic_2_1.loc[
            (statistic_2_1["id"] == int(feature_id))] if statistic_2_1 is not None else None
        statistic_3_filtered = statistic_3.loc[
            (statistic_3["id"] == int(feature_id))] if statistic_3 is not None else None
        statistic_4_1_filtered = statistic_4_1.loc[
            (statistic_4_1["id"] == int(feature_id))] if statistic_4_1 is not None else None

        # Check for missing data
        if statistic_1_filtered is not None and statistic_1_filtered.shape[0] == 0:
            print(f"✗️ No planning area data in {statistic_name}-1 for id={feature_id}")
        if statistic_2_1_filtered is not None and statistic_2_1_filtered.shape[0] == 0:
            print(f"✗️ No planning area data in {statistic_name}-2-1 for id={feature_id}")
        if statistic_3_filtered is not None and statistic_3_filtered.shape[0] == 0:
            print(f"✗️ No planning area data in {statistic_name}-3 for id={feature_id}")
        if statistic_4_1_filtered is not None and statistic_4_1_filtered.shape[0] == 0:
            print(f"✗️ No planning area data in {statistic_name}-4-1 for id={feature_id}")

        # Blend data
        feature = blend_planning_area_data_post_2020(
            feature=feature, area_sqkm=area_sqkm,
            statistic_1_filtered=statistic_1_filtered,
            statistic_2_1_filtered=statistic_2_1_filtered,
            statistic_3_filtered=statistic_3_filtered,
            statistic_4_1_filtered=statistic_4_1_filtered
        )

        # Build structure
        if year not in statistics:
            statistics[year] = {}
        if half_year not in statistics[year]:
            statistics[year][half_year] = {}

        # Add properties
        statistics[year][half_year][feature_id] = feature["properties"]

    # Calculate average and median values
    for year, half_years in statistics.items():
        for half_year, feature_ids in half_years.items():
            values = {}

            for feature_id, properties in feature_ids.items():
                for property_name, property_value in properties.items():
                    if property_name in statistic_properties:
                        if property_name not in values:
                            values[property_name] = []
                        values[property_name].append(property_value)

            statistics[year][half_year]["average"] = {key: stats.mean(lst) for key, lst in values.items()}
            statistics[year][half_year]["median"] = {key: stats.median(lst) for key, lst in values.items()}

    return geojson_extended, statistics


def blend_district_data(feature, area_sqkm, statistic_2_3_filtered, statistic_4_3_filtered):
    # Add new properties
    add_property_with_modifiers(feature, statistic_2_3_filtered, "inhabitants", area_sqkm)

    for property_name in statistic_properties:
        add_property(feature, statistic_2_3_filtered, property_name)
    for property_name in statistic_properties:
        add_property(feature, statistic_4_3_filtered, property_name)

    return feature


def blend_district_region_data(feature, area_sqkm, statistic_2_2_filtered, statistic_4_2_filtered):
    # Add new properties
    add_property_with_modifiers(feature, statistic_2_2_filtered, "inhabitants", area_sqkm)

    for property_name in statistic_properties:
        add_property(feature, statistic_2_2_filtered, property_name)
    for property_name in statistic_properties:
        add_property(feature, statistic_4_2_filtered, property_name)

    return feature


def blend_planning_area_data(feature, area_sqkm, statistic_1_filtered, statistic_2_1_filtered, statistic_3_filtered,
                             statistic_4_1_filtered):
    # Add new properties
    add_property_with_modifiers(feature, statistic_1_filtered, "inhabitants", area_sqkm)

    for property_name in statistic_properties:
        add_property(feature, statistic_1_filtered, property_name)
    for property_name in statistic_properties:
        add_property(feature, statistic_2_1_filtered, property_name)
    for property_name in statistic_properties:
        add_property(feature, statistic_3_filtered, property_name)
    for property_name in statistic_properties:
        add_property(feature, statistic_4_1_filtered, property_name)

    return feature


def blend_district_data_post_2020(feature, area_sqkm, statistic_2_3_filtered, statistic_4_3_filtered):
    # Add new properties
    add_property_with_modifiers(feature, statistic_2_3_filtered, "inhabitants", area_sqkm)

    for property_name in statistic_properties:
        add_property(feature, statistic_2_3_filtered, property_name)
    for property_name in statistic_properties:
        add_property(feature, statistic_4_3_filtered, property_name)

    return feature


def blend_district_region_data_post_2020(feature, area_sqkm, statistic_2_2_filtered, statistic_4_2_filtered):
    # Add new properties
    add_property_with_modifiers(feature, statistic_2_2_filtered, "inhabitants", area_sqkm)

    for property_name in statistic_properties:
        add_property(feature, statistic_2_2_filtered, property_name)
    for property_name in statistic_properties:
        add_property(feature, statistic_4_2_filtered, property_name)

    return feature


def blend_planning_area_data_post_2020(feature, area_sqkm, statistic_1_filtered, statistic_2_1_filtered,
                                       statistic_3_filtered, statistic_4_1_filtered):
    # Add new properties
    add_property_with_modifiers(feature, statistic_1_filtered, "inhabitants", area_sqkm)

    for property_name in statistic_properties:
        add_property(feature, statistic_1_filtered, property_name)
    for property_name in statistic_properties:
        add_property(feature, statistic_2_1_filtered, property_name)
    for property_name in statistic_properties:
        add_property(feature, statistic_3_filtered, property_name)
    for property_name in statistic_properties:
        add_property(feature, statistic_4_1_filtered, property_name)

    return feature


def add_property(feature, statistics, property_name):
    if statistics is not None and property_name in statistics:
        try:
            feature["properties"][f"{property_name}"] = float(statistics[property_name])
        except ValueError:
            feature["properties"][f"{property_name}"] = 0
        except TypeError:
            feature["properties"][f"{property_name}"] = 0


def add_property_with_modifiers(feature, statistics, property_name, total_area_sqkm):
    if statistics is not None and property_name in statistics:
        try:
            feature["properties"][f"{property_name}"] = float(statistics[property_name].sum())
            if total_area_sqkm is not None:
                feature["properties"][f"{property_name}_per_sqkm"] = round(
                    float(statistics[property_name].sum()) / total_area_sqkm)
        except ValueError:
            feature["properties"][f"{property_name}"] = 0

            if total_area_sqkm is not None:
                feature["properties"][f"{property_name}_per_sqkm"] = 0
        except TypeError:
            feature["properties"][f"{property_name}"] = 0

            if total_area_sqkm is not None:
                feature["properties"][f"{property_name}_per_sqkm"] = 0
