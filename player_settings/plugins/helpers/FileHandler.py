import csv
import json
import logging
import re
from os import listdir, mkdir
from os.path import join, isfile, isdir, sep, abspath, dirname

from player_settings.plugins.helpers.eye_movements.Fixation import *
from player_settings.plugins.helpers.eye_movements.Saccade import *
from player_settings.plugins.helpers.eye_movements.PSO import *
from player_settings.plugins.helpers.eye_movements.SmoothPursuit import *
from player_settings.plugins.helpers.FixationReport import FixationReport
from player_settings.plugins.helpers.GazePoint import GazePoint
from player_settings.plugins.helpers.Surface import Surface
from player_settings.plugins.helpers.properties.log_messages import *
from player_settings.plugins.helpers.properties.properties import not_defined_area

logger = logging.getLogger(__name__)


class FileHandler(object):
    confidence_treshold = 0.6
    pupil_helpers_dir = dirname(abspath(__file__))

    @staticmethod
    def __create_directory__(location, name):
        filepath = join(location, name)
        if not isdir(filepath):
            print("Creating /{} directory...".format(name))
            mkdir(filepath)
        return filepath

    def is_data_confident(self, csv_row):
        return float(csv_row['confidence']) > self.confidence_treshold

    @staticmethod
    def log_loading_data_from_file(filename):
        print('\n\nLoading data from file\n\t {}'.format(filename))

    @staticmethod
    def is_data_on_surface(csv_row):
        if 'on_srf' in csv_row:  # v <= 1.12
            return csv_row['on_srf'] == "True"
        if 'on_surf' in csv_row:  # v >= 1.13
            return csv_row['on_surf'] == "True"

    def __init__(self, g_pool):
        self.base_dir = g_pool.user_dir.rsplit(sep, 1)[0]  # {HOME}\pupil
        self.user_dir = g_pool.user_dir  # self.base_dir\
        self.fonts_dir = join(self.pupil_helpers_dir, 'fonts')
        self.recording_dir = g_pool.rec_dir

        # TODO: check; info.csv or export_info.csv in old versions
        # self.info_file = join(self.recording_dir, "info.old_style.csv")
        self.info_file = join(self.recording_dir, "info.player.json")

        self.exports_dir = self.get_recent_exported_dir_path()

        if self.exports_dir is not None:
            self.fixations_numpy_timestamps_file = join(self.recording_dir, "fixations_timestamps.npy")
            self.fixation_report_file = join(self.exports_dir, "fixation_report.csv")
            self.fixations_file = join(self.exports_dir, "fixations.csv")

            self.eye_movement_by_gaze_file = join(self.exports_dir, "eye_movement_by_gaze.csv")
            self.eye_movement_by_segment_file = join(self.exports_dir, "eye_movement_by_segment.csv")
            # self.gaze_positions_file = join(self.exports_dir, "gaze_positions.csv") # not used
            # self.pupil_positions_file = join(self.exports_dir, "pupil_positions.csv") # not used

            self.surfaces_path = join(self.exports_dir, "surfaces")
            if isdir(self.surfaces_path):
                self.surface_gaze_distribution_file = join(self.surfaces_path, "surface_gaze_distribution.csv")
                # self.surfaces_visibility_file = join(self.surfaces_path, "surface_visibility.csv") # not used
                # self.surface_events_file = join(self.surfaces_path, "surface_events.csv") # not used
            else:
                logger.error(not_found_surfaces_dir_info.format(self.exports_dir))

            self.downloads_dir = FileHandler.__create_directory__(location=self.exports_dir, name="downloads")
            self.images_dir = FileHandler.__create_directory__(location=self.downloads_dir, name="images")

            self.fixations_indexes_on_defined_surf = set()

    def get_recent_exported_dir_path(self):
        """
            This method finds the latest exported directory of current recording.
        """
        try:
            exports_dir = join(self.recording_dir, "exports")
            latest = None

            if isdir(exports_dir):
                exports_subdirectories = sorted(listdir(exports_dir))
                print(">>> exports_subdirectories", exports_subdirectories)
                latest = join(exports_dir, exports_subdirectories[len(exports_subdirectories) - 1])
                print("The latest directory in \\exports: \n", latest)
            else:
                logger.error(not_found_exports_dir_info.format(self.recording_dir))
            return latest
        except Exception:
            logger.error("No /exports directory found. Export data using Raw Data Exporter plugin")

    #########################################################
    #       loading raw data from CSV exported files
    #########################################################

    def load_recording_info(self):
        basic_rec_info_dict = {}
        print("Load export info data from ", self.info_file)
        if isfile(self.info_file):

            with open(self.info_file) as json_file:
                data = json.load(json_file)
                print(data["duration_s"])
                print(data["meta_version"])
                print(data["min_player_version"])
                print(data["recording_name"])
                print(data["recording_software_name"])
                print(data["recording_software_version"])
                print(data["recording_uuid"])
                print(data["start_time_synced_s"])
                print(data["start_time_system_s"])
                print(data["system_info"])
                basic_rec_info_dict = data

            # with open(file=self.info_file, newline='') as file:
            #     dict_reader = csv.DictReader(file)
            #     for row in dict_reader:
            #         basic_rec_info_dict[row["key"]] = row["value"]
            #     file.close()
            print(basic_rec_info_dict)
            return basic_rec_info_dict
        else:
            logger.error("NOT FOUND: info.csv")

    # fixation_report.csv
    def load_fixation_report_data(self):
        """
            Loads basic data about fixations:
            (parameters on the basis of which fixations identification was made)
            - max_dispersion
            - min_duration
            - max_duration
            - fixation_count
        """
        if isfile(self.fixation_report_file):
            with open(self.fixation_report_file, newline='') as file:
                dict_reader = csv.DictReader(file)
                dictionary = {}
                for row in dict_reader:
                    # print(row['fixation classifier'], row['Dispersion_Duration'])
                    if row['fixation classifier'] is not "":
                        dictionary[row['fixation classifier']] = row['Dispersion_Duration']
                file.close()

            fixation_report_obj = FixationReport(dictionary)
            print(fixation_report_obj.to_string())
            return fixation_report_obj
        else:
            logger.error("NOT FOUND: fixation_report.csv")

    # surfaces/surface_gaze_distribution.csv - no "confidence" provided in file
    def load_surfaces_gaze_data(self):
        """
            Loads basic data about surfaces:
            - total_gaze_point_count
            - surface_name and its gaze_count
        """
        if isdir(self.surfaces_path):
            if isfile(self.surface_gaze_distribution_file):
                with open(self.surface_gaze_distribution_file, newline='') as file:
                    total_gaze_point_count = int(file.readline()[23:])
                    # print("total_gaze_point_count: ", total_gaze_point_count)
                    next(file)  # omit blank row

                    dictionary = csv.DictReader(file)
                    surfaces_objects_dict = {}  # dict (surface_name, Surface instance)
                    for row in dictionary:
                        # print(row['surface_name'], row['gaze_count'])
                        name = row["surface_name"]
                        gaze_count = row["gaze_count"]
                        surfaces_objects_dict[name] = Surface(name, gaze_count)
                    file.close()
                # for key, value in surfaces_objects_dict.items():
                #     print(value.to_string())  # debug logging
                return surfaces_objects_dict, total_gaze_point_count
        #     else:
        #         logger.error("NOT FOUND: surface_gaze_distribution.csv")
        else:
            logger.error("NOT FOUND: /surfaces directory")

    # surfaces/fixations_on_surface_X.csv - no "confidence" provided in file
    # TODO deprecated
    def load_fixations_data_for_each_defined_surface(self, surfaces_objects_dict):
        """
            Loads data about fixations on given surface i.e.
            - id (ids from all these files = ids from fixations.csv file)
            - start_timestamp
            - duration
            - start_frame	and     end_frame
            - norm_pos_x	and     norm_pos_y
            - x_scaled	    and     y_scaled
            - on_srf

            from file with prefix "fixations_on_surface_".

            Data is filtered by "on_surf" parameter.
            Confidence is probably above 0.6 (like in fixations.csv file where all fixations are placed).

            :param surfaces_objects_dict: dictionary (K: surface name, V: Surface object)
        """
        if surfaces_objects_dict is not None:
            for surface_name, surface_obj in surfaces_objects_dict.items():

                for filename in listdir(self.surfaces_path):
                    if re.search("fixations_on_surface_{}.+".format(surface_name), filename):
                        self.log_loading_data_from_file(filename)

                        with open(join(self.surfaces_path, filename), newline='') as file:
                            dict_reader = csv.DictReader(file)
                            for row in dict_reader:
                                if self.is_data_on_surface(row):
                                    # print(row)  # OrderedDict([('id', '24'), ... ])
                                    fixation_obj = Fixation(row)
                                    # print(fixation_obj.to_string())
                                    fixation_id = fixation_obj.get_id()
                                    surface_obj.add_fixation_to_surface_list(fixation_obj)

                                    if fixation_id not in self.fixations_indexes_on_defined_surf:
                                        self.fixations_indexes_on_defined_surf.add(fixation_id)
                                    else:
                                        print("\tINFO: Fixation #{} detected on more than one surface".format(
                                            fixation_id))
                            #                                 # else:
                            #                                 #     print("Fixation #{} not on defined surface (on_srf = False)".format(fixation_id))
                            #     if fixation_id not in self.fixations_indexes_list:
                            #         not_on_any_surface_obj = surfaces_objects_dict['not_on_any_surface']
                            #         not_on_any_surface_obj.add_fixation_to_surface_list(fixation_obj)
                            #         self.fixations_indexes_list.append(fixation_id)
                            #                                 #     else:
                            #                                 #         print("Fixation #{} had already been loaded".format(fixation_id))
                            file.close()
        else:
            logger.error("NOT FOUND data about defined surfaces. Check if /surfaces directory exists.")

    # fixations.csv - "confidence" already > 0.6
    def load_fixations_data_for_not_defined_surf(self, surfaces_objects_dict):
        """
        Loading fixations which were detected out of defined surfaces.
        Confidence in fixations.csv already > 0.6
        No info about "on_srf" parameter.
        """
        if isfile(self.fixations_file):
            with open(file=self.fixations_file, newline='') as file:
                dict_reader = csv.DictReader(file)
                for row in dict_reader:
                    # print(row)  # OrderedDict([('id', '24'), ... ])
                    if row['id'] not in self.fixations_indexes_on_defined_surf:
                        fixation_obj = Fixation(row)
                        # add "not_on_any_surface" key to surfaces map <surface_name, Surface obj>
                        not_on_any_surface_obj = surfaces_objects_dict[not_defined_area]
                        not_on_any_surface_obj.add_fixation_to_surface_list(fixation_obj)
                file.close()
        else:
            logger.error("NOT FOUND: fixations.csv")

    def load_numpy_fixations_file(self):
        import numpy as np
        print("NUMPY FIXATIONS DATAAA")
        print(np.load(self.fixations_numpy_timestamps_file))

    def load_gaze_points_for_each_defined_surface(self, surfaces_objects_dict):
        if surfaces_objects_dict is not None:
            for surface_name, surface_obj in surfaces_objects_dict.items():

                for filename in listdir(self.surfaces_path):
                    if re.search(f"gaze_positions_on_surface_{surface_name}.+", filename):
                        self.log_loading_data_from_file(filename)

                        with open(join(self.surfaces_path, filename), newline='') as file:
                            dict_reader = csv.DictReader(file)
                            for row in dict_reader:
                                # print(row)  # OrderedDict([('id', '24'), ... ])
                                if self.is_data_on_surface(row) and self.is_data_confident(row):
                                    gaze_point_obj = GazePoint(row["x_scaled"], row["y_scaled"])
                                    surface_obj.add_gaze_point_to_list(gaze_point_obj)

                                    norm_gaze_point_obj = GazePoint(row["x_norm"], row["y_norm"])
                                    surface_obj.add_normalized_gaze_point_to_list(norm_gaze_point_obj)

    # not used
    def load_eye_movement_by_gaze(self):
        filename = self.eye_movement_by_gaze_file  # eye_movement_by_gaze.csv

        eye_movement_dict = {}
        fixations_count, saccades_count, pso_count, smooth_pursuit_count = 0, 0, 0, 0

        if isfile(filename):
            self.log_loading_data_from_file(filename)

            with open(filename, newline='') as file:
                dictionary = csv.DictReader(file)
                for row in dictionary:
                    # print(row['gaze_timestamp'], row['movement_class'])
                    if row["movement_class"] == "fixation":
                        fixations_count += 1
                    elif row["movement_class"] == "saccade":
                        saccades_count += 1
                    elif row["movement_class"] == "pso":
                        pso_count += 1
                    elif row["movement_class"] == "smooth_pursuit":
                        smooth_pursuit_count += 1

            eye_movement_dict["fixation"] = fixations_count
            eye_movement_dict["saccade"] = saccades_count
            eye_movement_dict["pso"] = pso_count
            eye_movement_dict["smooth_pursuit"] = smooth_pursuit_count
        else:
            logger.warning("NOT FOUND: /exports/eye_movement_by_gaze.csv")
            return eye_movement_dict

    def load_eye_movement_by_segment(self):
        filename = self.eye_movement_by_segment_file  # eye_movement_by_segment.csv

        all_eye_movement_dict = {}
        fixations_list, saccades_list, pso_list, smooth_pursuit_list = [], [], [], []

        if isfile(filename):
            self.log_loading_data_from_file(filename)

            with open(filename, newline='') as file:
                dictionary = csv.DictReader(file)
                for row in dictionary:
                    if row["segment_class"] == "fixation":
                        fixations_list.append(Fixation(row))

                    elif row["segment_class"] == "saccade":
                        saccades_list.append(Saccade(row))

                    elif row["segment_class"] == "pso":
                        pso_list.append(PSO(row))

                    elif row["segment_class"] == "smooth_pursuit":
                        smooth_pursuit_list.append(SmoothPursuit(row))

            all_eye_movement_dict["fixation"] = fixations_list
            all_eye_movement_dict["saccade"] = saccades_list
            all_eye_movement_dict["pso"] = pso_list
            all_eye_movement_dict["smooth_pursuit"] = smooth_pursuit_list
        else:
            logger.warning("NOT FOUND: /exports/eye_movement_by_segment.csv")

        return all_eye_movement_dict
