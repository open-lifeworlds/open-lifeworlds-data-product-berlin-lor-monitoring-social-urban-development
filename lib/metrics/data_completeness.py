import json
import os
import unittest

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

data_path = os.path.join(script_path, "..", "..", "data")

key_figure_group = "berlin-lor-monitoring-social-urban-development"

statistic_fields = [
    "inhabitants",
    "s1_percentage_unemployed",
    "s2_percentage_long_term_unemployed"
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

statistic_properties = statistic_fields


class FilesTestCase(unittest.TestCase):
    pass


for year in [2013, 2015, 2017, 2019, 2021]:
    for half_year in ["00"]:
        for lor_area_type in ["districts", "district-regions", "planning-areas"]:
            file = os.path.join(data_path, f"{key_figure_group}-{year}-{half_year}",
                                f"{key_figure_group}-{year}-{half_year}-{lor_area_type}.geojson")
            setattr(
                FilesTestCase,
                f"test_{key_figure_group}_{year}_{half_year}_{lor_area_type}".replace('-', '_'),
                lambda self, file=file: self.assertTrue(os.path.exists(file))
            )


class Properties2013TestCase(unittest.TestCase):
    pass


class Properties2015TestCase(unittest.TestCase):
    pass


class Properties2017TestCase(unittest.TestCase):
    pass


class Properties2019TestCase(unittest.TestCase):
    pass


class Properties2021TestCase(unittest.TestCase):
    pass


def get_test_case(year):
    if year == 2013:
        return Properties2013TestCase
    if year == 2015:
        return Properties2015TestCase
    if year == 2017:
        return Properties2017TestCase
    if year == 2019:
        return Properties2019TestCase
    if year == 2021:
        return Properties2021TestCase


for year in [2013, 2015, 2017, 2019, 2021]:
    for half_year in ["00"]:
        for lor_area_type in ["districts", "district-regions", "planning-areas"]:
            file = os.path.join(data_path, f"{key_figure_group}-{year}-{half_year}",
                                f"{key_figure_group}-{year}-{half_year}-{lor_area_type}.geojson")
            if os.path.exists(file):
                with open(file=file, mode="r", encoding="utf-8") as geojson_file:
                    geojson = json.load(geojson_file, strict=False)

                for feature in geojson["features"]:
                    feature_id = feature["properties"]["id"]

                    setattr(
                        get_test_case(year),
                        f"test_{key_figure_group}_{year}_{half_year}_{lor_area_type}_{feature_id}".replace('-', '_'),
                        lambda self, feature=feature: self.assertTrue(
                            all(prop in feature["properties"] for prop in statistic_properties))
                    )

                    # for property in statistic_properties:
                    #     setattr(
                    #         get_test_case(year),
                    #         f"test_{key_figure_group}_{year}_{half_year}_{lor_area_type}_{feature_id}_{property}"
                    #             .replace('-', '_'),
                    #         lambda self, feature=feature, property=property: self.assertTrue(
                    #             property in feature["properties"])
                    #     )

if __name__ == '__main__':
    unittest.main()
