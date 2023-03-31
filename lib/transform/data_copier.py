import os
import shutil

from lib.tracking_decorator import TrackingDecorator


@TrackingDecorator.track_time
def copy_data(source_path, results_path, clean=False, quiet=False):
    # Iterate over files
    for subdir, dirs, files in sorted(os.walk(source_path)):
        for source_file_name in sorted(files):
            subdir = subdir.replace(f"{source_path}/", "")
            results_file_name = get_results_file_name(subdir, source_file_name)

            # Make results path
            os.makedirs(os.path.join(results_path, subdir), exist_ok=True)

            source_file_path = os.path.join(source_path, subdir, source_file_name)
            results_file_path = os.path.join(results_path, subdir, results_file_name)

            # Check if file needs to be copied
            if clean or not os.path.exists(results_file_path):
                shutil.copyfile(source_file_path, results_file_path)

                if not quiet:
                    print(f"✓ Copy {results_file_name}")
            else:
                print(f"✓ Already exists {results_file_name}")


def get_results_file_name(subdir, source_file_name):
    if source_file_name == "1-sdi_mss2013.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2013-00-1.xlsx"
    if source_file_name == "2-1-indexind_anteile_plr_mss2013.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2013-00-2-1.xlsx"
    if source_file_name == "2-2-indexind_anteile_bzr_mss2013.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2013-00-2-2.xlsx"
    if source_file_name == "2-3-indexind_anteile_bezirke_mss2013.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2013-00-2-3.xlsx"
    if source_file_name == "3-indexind_z_wertemss2013.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2013-00-3.xlsx"
    if source_file_name == "4-1-kontextind_anteile_plr_mss2013.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2013-00-4-1.xlsx"
    if source_file_name == "4-2-kontextind_anteile_bzr_mss2013.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2013-00-4-2.xlsx"
    if source_file_name == "4-3-kontextind_anteile_bezirke_mss2013.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2013-00-4-3.xlsx"
    if source_file_name == "1-sdi_mss2015.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2015-00-1.xlsx"
    if source_file_name == "2-1-indexind_anteile_plr_mss2015.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2015-00-2-1.xlsx"
    if source_file_name == "2-2-indexind_anteile_bzr_mss2015.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2015-00-2-2.xlsx"
    if source_file_name == "2-3-indexind_anteile_bezirke_mss2015.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2015-00-2-3.xlsx"
    if source_file_name == "3-indexind_z_wertemss2015.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2015-00-3.xlsx"
    if source_file_name == "4-1-kontextind_anteile_plr_mss2015.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2015-00-4-1.xlsx"
    if source_file_name == "4-2-kontextind_anteile_bzr_mss2015.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2015-00-4-2.xlsx"
    if source_file_name == "4-3-kontextind_anteile_bezirke_mss2015.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2015-00-4-3.xlsx"
    if source_file_name == "1-sdi_mss2017.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2017-00-1.xlsx"
    if source_file_name == "2-1-indexind_anteile_plr_mss2017.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2017-00-2-1.xlsx"
    if source_file_name == "2-2-indexind_anteile_bzr_mss2019.xlsx" and subdir == "berlin-lor-monitoring-social-urban-development-2017-00":
        return "berlin-lor-monitoring-social-urban-development-2017-00-2-2.xlsx"
    if source_file_name == "2.3.indexind_anteile_bezirke_mss2017.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2017-00-2-3.xlsx"
    if source_file_name == "3-indexind_z_wertemss2017.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2017-00-3.xlsx"
    if source_file_name == "4-1-kontextind_anteile_plr_mss2017.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2017-00-4-1.xlsx"
    if source_file_name == "4-2-kontextind_anteile_bzr_mss2017.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2017-00-4-2.xlsx"
    if source_file_name == "4-3-kontextind_anteile_bezirke_mss2017.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2017-00-4-3.xlsx"
    if source_file_name == "1-sdi_mss2019.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2019-00-1.xlsx"
    if source_file_name == "2-1-indexind_anteile_plr_mss2019.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2019-00-2-1.xlsx"
    if source_file_name == "2-2-indexind_anteile_bzr_mss2019.xlsx" and subdir == "berlin-lor-monitoring-social-urban-development-2019-00":
        return "berlin-lor-monitoring-social-urban-development-2019-00-2-2.xlsx"
    if source_file_name == "2-3-indexind_anteile_bezirke_mss2019.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2019-00-2-3.xlsx"
    if source_file_name == "3-indexind_z_wertemss2019.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2019-00-3.xlsx"
    if source_file_name == "4.1.kontextind_anteile_plr_mss2019.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2019-00-4-1.xlsx"
    if source_file_name == "4.2.kontextind_anteile_bzr_mss2019.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2019-00-4-2.xlsx"
    if source_file_name == "4.3.kontextind_anteile_bezirke_mss2019.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2019-00-4-3.xlsx"
    if source_file_name == "tabelle_1_gesamtindex_soziale_ungleichheit_sdi_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-1.xlsx"
    if source_file_name == "tabelle_2-1_index-indikatoren_anteilswerte_auf_planungsraum-ebene_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-2-1.xlsx"
    if source_file_name == "tabelle_2-2_index-indikatoren_anteilswerte_auf_bezirksregionen-ebene_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-2-2.xlsx"
    if source_file_name == "tabelle_2-3_index-indikatoren_auf_ebene_der_bezirke_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-2-3.xlsx"
    if source_file_name == "tabelle_3_index-indikatoren_z-werte_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-3.xlsx"
    if source_file_name == "tabelle_4-1_kontext-indikatoren_anteile_plr_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-4-1.xlsx"
    if source_file_name == "tabelle_4-2_kontext-indikatoren_anteile_bzr_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-4-2.xlsx"
    if source_file_name == "tabelle_4-3_kontext-indikatoren_anteile_bezirke_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-4-3.xlsx"
    if source_file_name == "tabelle_4-1-1_kontext-indikatoren_anteile_plr_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-4-1-1.xlsx"
    if source_file_name == "tabelle_4-2-1_kontext-indikatoren_anteile_bzr_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-4-2-1.xlsx"
    if source_file_name == "tabelle_4-3-1_kontext-indikatoren_anteile_bezirke_mss_2021.xlsx":
        return "berlin-lor-monitoring-social-urban-development-2021-00-4-3-1.xlsx"
    else:
        return source_file_name
