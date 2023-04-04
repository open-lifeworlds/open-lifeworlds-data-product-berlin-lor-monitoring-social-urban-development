import os
import re

import pandas as pd

from lib.tracking_decorator import TrackingDecorator


@TrackingDecorator.track_time
def convert_data_to_csv(source_path, results_path, clean=False, quiet=False):
    # Iterate over files
    for subdir, dirs, files in sorted(os.walk(source_path)):

        # Make results path
        subdir = subdir.replace(f"{source_path}/", "")
        os.makedirs(os.path.join(results_path, subdir), exist_ok=True)

        source_file_paths_planning_areas = []
        source_file_paths_district_regions = []
        source_file_paths_districts = []

        # Split files by LOR area type
        for file_name in sorted(files):
            source_file_path = os.path.join(source_path, subdir, file_name)

            if re.search(r"\d{4}-\d{2}-1.xlsx", file_name) is not None \
                    or re.search(r"\d{4}-\d{2}-2-1.xlsx", file_name) is not None \
                    or re.search(r"\d{4}-\d{2}-3.xlsx", file_name) is not None \
                    or re.search(r"\d{4}-\d{2}-4-1.xlsx", file_name) is not None:
                source_file_paths_planning_areas.append(source_file_path)
            elif re.search(r"\d{4}-\d{2}-2-2.xlsx", file_name) is not None or \
                    re.search(r"\d{4}-\d{2}-4-2.xlsx", file_name) is not None:
                source_file_paths_district_regions.append(source_file_path)
            elif re.search(r"\d{4}-\d{2}-2-3.xlsx", file_name) is not None \
                    or re.search(r"\d{4}-\d{2}-4-3.xlsx", file_name) is not None:
                source_file_paths_districts.append(source_file_path)

        if len(source_file_paths_planning_areas) > 0 and len(source_file_paths_district_regions) > 0 and len(
                source_file_paths_districts) > 0:
            convert_file_to_csv_planning_areas(source_file_paths_planning_areas, clean=clean, quiet=quiet)
            convert_file_to_csv_district_regions(source_file_paths_district_regions, clean=clean, quiet=quiet)
            convert_file_to_csv_districts(source_file_paths_districts, clean=clean, quiet=quiet)


def convert_file_to_csv_planning_areas(source_file_paths, clean=False, quiet=False):
    pattern = r".*\d{4}-\d{2}"
    file_path_csv = os.path.join(os.path.dirname(source_file_paths[0]),
                                 f"{re.match(pattern, os.path.basename(source_file_paths[0])).group()}-planning-areas.csv")

    # Check if result needs to be generated
    if clean or not os.path.exists(file_path_csv):
        dataframes = []

        try:
            for source_file_path in source_file_paths:
                source_file_name, source_file_extension = os.path.splitext(source_file_path)

                if source_file_extension == ".xlsx":
                    engine = "openpyxl"
                elif source_file_extension == ".xls":
                    engine = None
                else:
                    return

                # Set default values
                drop_columns = []

                year = os.path.basename(source_file_name).split(sep="-")[6]

                if re.search(r"\d{4}-\d{2}-1", source_file_name) is not None:

                    sheets = [f"1.SDI_MSS{year}"]
                    skiprows = 3
                    names = ["id", "name", "inhabitants", "status_index", "status_index_class", "dynamic_index",
                             "dynamic_index_class", "status_dynamic_index", "status_dynamic_index_class"]
                elif re.search(r"\d{4}-\d{2}-2-1", source_file_name) is not None:

                    sheets = [f"2.1.IndexInd_Ant_PLR_MSS{year}"]
                    skiprows = 8
                    names = [
                        "id", "name", "inhabitants", "s1_percentage_unemployed", "s2_percentage_long_term_unemployed",
                        "s3_percentage_transfer_payments_recipients",
                        "s4_percentage_transfer_payments_recipients_below_15_years", "d1_percentage_unemployed",
                        "d2_percentage_long_term_unemployed", "d3_percentage_transfer_payments_recipients",
                        "d4_percentage_transfer_payments_recipients_below_15_years"
                    ]
                    if year == "2019" or year == "2021":
                        drop_columns = ["name", "average_and_standard_deviation", "s2_percentage_long_term_unemployed",
                                        "d2_percentage_long_term_unemployed"]
                    else:
                        drop_columns = ["name", "average_and_standard_deviation"]
                elif re.search(r"\d{4}-\d{2}-3", source_file_name) is not None:

                    if year == "2017":
                        sheets = [f"3.IndexInd_z_Werte_MSS2015"]
                    else:
                        sheets = [f"3.IndexInd_z_Werte_MSS{year}"]
                    skiprows = 15
                    names = [
                        "id", "name", "inhabitants", "z_s1_percentage_unemployed",
                        "z_s2_percentage_long_term_unemployed", "z_s3_percentage_transfer_payments_recipients",
                        "z_s4_percentage_transfer_payments_recipients_below_15_years", "z_d1_percentage_unemployed",
                        "z_d2_percentage_long_term_unemployed", "z_d3_percentage_transfer_payments_recipients",
                        "z_d4_percentage_transfer_payments_recipients_below_15_years"
                    ]
                    if year == "2019" or year == "2021":
                        drop_columns = ["name", "average_and_standard_deviation",
                                        "z_s2_percentage_long_term_unemployed", "z_d2_percentage_long_term_unemployed"]
                    else:
                        drop_columns = ["name", "average_and_standard_deviation"]
                elif re.search(r"\d{4}-\d{2}-4-1", source_file_name) is not None:

                    if year == "2013":
                        sheets = [f"Kontextind_MSS{year}_PLR"]
                    elif year == "2017":
                        sheets = [f"4.1.KontextInd_MSS2015"]
                    else:
                        sheets = [f"4.1.KontextInd_MSS{year}"]

                    if year == "2021":
                        skiprows = 18
                        names = [
                            "id", "name", "inhabitants", "average_and_standard_deviation", "k01_youth_unemployment",
                            "k02_single_parent_households", "k03_old_age_poverty",
                            "k04_children_with_migration_background", "k05_inhabitants_with_migration_background",
                            "k16_foreigners", "k06_change_proportion_of_foreigner", "k17_non_eu_foreigners",
                            "k07_foreign_transfer_recipients", "k08_urban_apartments", "k14_living_rooms",
                            "k15_living_space", "k09_simple_residential_area", "k10_duration_of_residence_over_5_years",
                            "k11_migration_volume", "k12_balance_of_migration",
                            "k13_balance_of_migration_of_children_below_6"
                        ]
                        drop_columns = ["name", "average_and_standard_deviation", "k08_urban_apartments",
                                        "k14_living_rooms", "k15_living_space"]
                    else:
                        skiprows = 15
                        names = [
                            "id", "name", "inhabitants", "average_and_standard_deviation", "k01_youth_unemployment",
                            "k02_single_parent_households", "k03_old_age_poverty",
                            "k04_children_with_migration_background",
                            "k05_inhabitants_with_migration_background", "k06_change_proportion_of_foreigner",
                            "k07_foreign_transfer_recipients", "k08_urban_apartments", "k09_simple_residential_area",
                            "k10_duration_of_residence_over_5_years", "k11_migration_volume",
                            "k12_balance_of_migration", "k13_balance_of_migration_of_children_below_6"
                        ]
                        drop_columns = ["name", "average_and_standard_deviation"]
                else:
                    sheets = []
                    skiprows = 0
                    names = []
                    drop_columns = []

                for sheet in sheets:
                    dataframes.append(
                        pd.read_excel(source_file_path, engine=engine, sheet_name=sheet, skiprows=skiprows,
                                      usecols=list(range(0, len(names))), names=names)
                        .drop(columns=drop_columns, errors="ignore")
                        .dropna())

            # Concatenate data frames
            dataframe = pd.concat([df.set_index("id") for df in dataframes], axis=1).reset_index().dropna()

            # Write csv file
            if dataframe.shape[0] > 0:
                dataframe.to_csv(file_path_csv, index=False)
                if not quiet:
                    print(f"✓ Convert {file_path_csv}")
            else:
                if not quiet:
                    print(dataframe.head())
                    print(f"✗️ Empty {file_path_csv}")
        except Exception as e:
            print(f"✗️ Exception: {str(e)}")
    elif not quiet:
        print(f"✓ Already exists {file_path_csv}")


def convert_file_to_csv_district_regions(source_file_paths, clean=False, quiet=False):
    pattern = r".*\d{4}-\d{2}"
    file_path_csv = os.path.join(os.path.dirname(source_file_paths[0]),
                                 f"{re.match(pattern, os.path.basename(source_file_paths[0])).group()}-district-regions.csv")

    # Check if result needs to be generated
    if clean or not os.path.exists(file_path_csv):
        dataframes = []

        try:
            for source_file_path in source_file_paths:
                source_file_name, source_file_extension = os.path.splitext(source_file_path)

                if source_file_extension == ".xlsx":
                    engine = "openpyxl"
                elif source_file_extension == ".xls":
                    engine = None
                else:
                    return

                # Set default values
                drop_columns = []

                year = os.path.basename(source_file_name).split(sep="-")[6]

                if re.search(r"\d{4}-\d{2}-2-2", source_file_name) is not None:

                    if year == "2017":
                        sheets = [f"2.2.IndexInd_Ant_BZR_MSS2019"]
                    else:
                        sheets = [f"2.2.IndexInd_Ant_BZR_MSS{year}"]
                    skiprows = 12
                    names = [
                        "id", "name", "inhabitants", "s1_percentage_unemployed",
                        "s2_percentage_long_term_unemployed",
                        "s3_percentage_transfer_payments_recipients",
                        "s4_percentage_transfer_payments_recipients_below_15_years", "d1_percentage_unemployed",
                        "d2_percentage_long_term_unemployed", "d3_percentage_transfer_payments_recipients",
                        "d4_percentage_transfer_payments_recipients_below_15_years"
                    ]
                    if year == "2017" or year == "2019" or year == "2021":
                        drop_columns = ["name", "average_and_standard_deviation", "s2_percentage_long_term_unemployed",
                                        "d2_percentage_long_term_unemployed"]
                    else:
                        drop_columns = ["name", "average_and_standard_deviation"]
                elif re.search(r"\d{4}-\d{2}-4-2", source_file_name) is not None:
                    if year == "2013":
                        sheets = [f"Kontextind_MSS{year}_BZR"]
                        skiprows = 16
                        names = [
                            "id", "name", "inhabitants", "average_and_standard_deviation", "k01_youth_unemployment",
                            "k02_single_parent_households", "k03_old_age_poverty",
                            "k04_children_with_migration_background",
                            "k05_inhabitants_with_migration_background", "k06_change_proportion_of_foreigner",
                            "k07_foreign_transfer_recipients", "k08_urban_apartments", "k09_simple_residential_area",
                            "k10_duration_of_residence_over_5_years", "k11_migration_volume",
                            "k12_balance_of_migration",
                            "k13_balance_of_migration_of_children_below_6"
                        ]
                    else:
                        sheets = [f"4.2.KontextInd_MSS{year}"]
                        skiprows = 16
                        names = [
                            "id", "name", "inhabitants", "average_and_standard_deviation", "k01_youth_unemployment",
                            "k02_single_parent_households", "k03_old_age_poverty",
                            "k04_children_with_migration_background",
                            "k05_inhabitants_with_migration_background", "k16_foreigners",
                            "k06_change_proportion_of_foreigner", "k17_non_eu_foreigners",
                            "k07_foreign_transfer_recipients", "k08_urban_apartments", "k14_living_rooms",
                            "k15_living_space", "k09_simple_residential_area", "k10_duration_of_residence_over_5_years",
                            "k11_migration_volume", "k12_balance_of_migration",
                            "k13_balance_of_migration_of_children_below_6"
                        ]

                    if year == "2021":
                        drop_columns = ["name", "average_and_standard_deviation", "k08_urban_apartments",
                                        "k14_living_rooms", "k15_living_space"]
                    else:
                        drop_columns = ["name", "average_and_standard_deviation"]
                else:
                    sheets = []
                    skiprows = 0
                    names = []
                    drop_columns = []

                for sheet in sheets:
                    dataframes.append(
                        pd.read_excel(source_file_path, engine=engine, sheet_name=sheet, skiprows=skiprows,
                                      usecols=list(range(0, len(names))), names=names)
                            .drop(columns=drop_columns, errors="ignore")
                            .dropna())

            # Concatenate data frames
            dataframe = pd.concat([df.set_index("id") for df in dataframes], axis=1).reset_index().dropna()

            # Write csv file
            if dataframe.shape[0] > 0:
                dataframe.to_csv(file_path_csv, index=False)
                if not quiet:
                    print(f"✓ Convert {file_path_csv}")
            else:
                if not quiet:
                    print(dataframe.head())
                    print(f"✗️ Empty {file_path_csv}")
        except Exception as e:
            print(f"✗️ Exception: {str(e)}")
    elif not quiet:
        print(f"✓ Already exists {file_path_csv}")


def convert_file_to_csv_districts(source_file_paths, clean=False, quiet=False):
    pattern = r".*\d{4}-\d{2}"
    file_path_csv = os.path.join(os.path.dirname(source_file_paths[0]),
                                 f"{re.match(pattern, os.path.basename(source_file_paths[0])).group()}-districts.csv")

    # Check if result needs to be generated
    if clean or not os.path.exists(file_path_csv):
        dataframes = []

        try:
            for source_file_path in source_file_paths:
                source_file_name, source_file_extension = os.path.splitext(source_file_path)

                if source_file_extension == ".xlsx":
                    engine = "openpyxl"
                elif source_file_extension == ".xls":
                    engine = None
                else:
                    return

                year = os.path.basename(source_file_name).split(sep="-")[6]

                if re.search(r"\d{4}-\d{2}-2-3", source_file_name) is not None:
                    if year == "2021":
                        sheets = ["2.3.IndexInd_Ant_Bezirk_MSS2021"]
                    else:
                        sheets = [f"2.3.IndexInd_Ant_BezirkeMSS{year}"]

                    skiprows = 8
                    names = [
                        "id", "name", "inhabitants", "s1_percentage_unemployed", "s2_percentage_long_term_unemployed",
                        "s3_percentage_transfer_payments_recipients",
                        "s4_percentage_transfer_payments_recipients_below_15_years", "d1_percentage_unemployed",
                        "d2_percentage_long_term_unemployed", "d3_percentage_transfer_payments_recipients",
                        "d4_percentage_transfer_payments_recipients_below_15_years"
                    ]
                    if year == "2019" or year == "2021":
                        drop_columns = ["average_and_standard_deviation", "s2_percentage_long_term_unemployed",
                                        "d2_percentage_long_term_unemployed"]
                    else:
                        drop_columns = ["average_and_standard_deviation"]
                elif re.search(r"\d{4}-\d{2}-4-3", source_file_name) is not None:
                    if year == "2013":
                        sheets = [f"Kontextind_MSS{year}_Bezirke"]
                        skiprows = 8
                        names = [
                            "id", "name", "inhabitants", "average_and_standard_deviation",
                            "k01_youth_unemployment", "k02_single_parent_households", "k03_old_age_poverty",
                            "k04_children_with_migration_background",
                            "k05_inhabitants_with_migration_background", "k06_change_proportion_of_foreigner",
                            "k07_foreign_transfer_recipients", "k08_urban_apartments", "k09_simple_residential_area",
                            "k10_duration_of_residence_over_5_years", "k11_migration_volume",
                            "k12_balance_of_migration",
                            "k13_balance_of_migration_of_children_below_6"
                        ]
                    else:
                        sheets = [f"4.3.KontextInd_MSS{year}"]
                        skiprows = 8
                        names = [
                            "id", "name", "inhabitants", "average_and_standard_deviation", "k01_youth_unemployment",
                            "k02_single_parent_households", "k03_old_age_poverty",
                            "k04_children_with_migration_background",
                            "k05_inhabitants_with_migration_background", "k16_foreigners",
                            "k06_change_proportion_of_foreigner", "k17_non_eu_foreigners",
                            "k07_foreign_transfer_recipients", "k08_urban_apartments", "k14_living_rooms",
                            "k15_living_space", "k09_simple_residential_area", "k10_duration_of_residence_over_5_years",
                            "k11_migration_volume", "k12_balance_of_migration",
                            "k13_balance_of_migration_of_children_below_6"
                        ]

                    if year == "2021":
                        drop_columns = ["average_and_standard_deviation", "k08_urban_apartments", "k14_living_rooms",
                                        "k15_living_space"]
                    else:
                        drop_columns = ["average_and_standard_deviation"]
                else:
                    sheets = []
                    skiprows = 0
                    names = []
                    drop_columns = []

                for sheet in sheets:
                    dataframes.append(
                        pd.read_excel(source_file_path, engine=engine, sheet_name=sheet, skiprows=skiprows,
                                      usecols=list(range(0, len(names))), names=names)
                            .drop(columns=drop_columns, errors="ignore")
                            .dropna())

            # Concatenate data frames
            dataframe = pd.concat([df.set_index("id") for df in dataframes], axis=1).reset_index().dropna()

            # Write csv file
            if dataframe.shape[0] > 0:
                dataframe.to_csv(os.path.basename(file_path_csv), index=False)
                if not quiet:
                    print(f"✓ Convert {os.path.basename(file_path_csv)}")
            else:
                if not quiet:
                    print(dataframe.head())
                    print(f"✗️ Empty {os.path.basename(file_path_csv)}")
        except Exception as e:
            print(f"✗️ Exception: {str(e)}")
    elif not quiet:
        print(f"✓ Already exists {os.path.basename(file_path_csv)}")
