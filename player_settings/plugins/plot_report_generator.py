"""
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2019 Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
"""
from os.path import join, isdir

from plugin import Plugin
from pyglui import ui

from player_settings.plugins.helpers.FileHandler import FileHandler
from player_settings.plugins.helpers.plots.EyeMovementsPlot import *
from player_settings.plugins.helpers.plots.FixationsDurationPlot import *
from player_settings.plugins.helpers.plots.FixationsFrequencyPlot import *
from player_settings.plugins.helpers.plots.FixationsPerSurfacePlot import *
from player_settings.plugins.helpers.plots.SaccadesPerSurfacePlot import *
from player_settings.plugins.helpers.plots.SurfaceVisibilityPlot import *
from player_settings.plugins.helpers.plots.HeatmapPlot import *
from player_settings.plugins.helpers.plots.Plot import *
from player_settings.plugins.helpers.Report import Report
from player_settings.plugins.helpers.properties.plugin_properties import *

from player_settings.plugins.helpers.properties import properties_pl
from player_settings.plugins.helpers.properties import properties

# logger = logging.getLogger(__name__)
logger = logging.getLogger()


class Plot_Report_Generator(Plugin):
    """ Generate report with various plots/diagrams/charts (based on exported raw data in Pupil Player) """

    order = 1
    uniqueness = "unique"
    icon_chr = chr(0xE01D)
    icon_font = "pupil_icons"

    def __init__(self, g_pool):
        super().__init__(g_pool)

        # definiowanie pozostałych pól klasy

        self.menu = None
        self.duration = g_pool.timestamps[-1] - g_pool.timestamps[0]  # duration of whole recording in seconds
        self.first_timestamp = g_pool.timestamps[0]

        # must have attr
        self.file_handler = None
        self.recording_info_dict = None
        self.surfaces_objects_dict = None  # dictionary of defined surfaces { surface_name: Surface object }
        self.total_gaze_point_count = None
        self.fixation_report = None  # Fixation Detector settings in Pupil Capture
        self.plots_dict = {}

        # plots options for generated report
        self.all_plots_flag = False

        self.surface_visibility_option = False
        self.fixations_per_surface_option = False
        self.fixations_frequency_option = False
        self.fixations_durations_option = False
        self.saccades_per_surface_option = False
        self.heatmaps_option = True
        self.eye_movements_option = True

        self.open_report_after_download_option = True
        self.pdf_report_file_name = ""

        self.language_option = report_eng_opt_label
        self.properties = properties

        self.data_generated = False

        self.all_eye_movement_dict = {}

        self.recording_dir = g_pool.rec_dir

    def init_ui(self):
        """ Plugin's UI (user interface) initialization """

        self.add_menu()
        self.menu.label = plugin_name  # nazwa pluginu

        general_informations = [
            ui.Info_Text(subtitle_1),
            ui.Info_Text(subtitle_2),
            ui.Info_Text(plots_options_description),
            ui.Button(mark_all_label, self.mark_all_plots),
        ]

        # opcje wykresów do wyboru
        plots_options = [
            ui.Switch("surface_visibility_option", self, label=surface_visibility_option_name),
            ui.Switch("heatmaps_option", self, label=heatmaps_option_name),
            # ui.Switch("eye_movements_option", self, label=eye_movements_option_name),
            ui.Switch("fixations_per_surface_option", self, label=fixations_per_surface_option_name),
            ui.Switch("fixations_frequency_option", self, label=fixations_frequency_option_name),
            ui.Switch("fixations_durations_option", self, label=fixations_durations_option_name),
            # ui.Switch("saccades_per_surface_option", self, label=saccades_per_surface_option_name)
        ]

        # ustawienia generowanego raportu
        report_options = [
            ui.Info_Text(report_download_description),
            ui.Selector("language_option", self, label=language_option_label,
                        selection=[report_eng_opt_label, report_pl_opt_label]),
            ui.Text_Input("pdf_report_file_name", self, label=report_name_label,
                          getter=lambda: report_name_placeholder_label),
            ui.Button(download_report_button_name, self.download_pdf_report),
            ui.Switch("open_report_after_download_option", self, label=open_report_after_download)
        ]

        menu_items = general_informations + plots_options + report_options

        for menu_item in menu_items:
            self.menu.append(menu_item)

    def deinit_ui(self):
        self.remove_menu()

    def get_init_dict(self):
        # all keys need to exists as keyword arguments in __init__ as well
        return {}

    #########################################################
    #                      custom methods
    #########################################################

    def mark_all_plots(self):
        self.all_plots_flag = False if self.all_plots_flag else True

        self.surface_visibility_option = self.all_plots_flag
        self.fixations_per_surface_option = self.all_plots_flag
        self.fixations_frequency_option = self.all_plots_flag
        self.fixations_durations_option = self.all_plots_flag
        self.saccades_per_surface_option = self.all_plots_flag
        self.heatmaps_option = self.all_plots_flag
        # self.eye_movements_option = self.all_plots_flag

    def is_data_exported(self):
        """
        Check if /exports directory exists
        :return: data_exported
        """
        data_exported = False
        try:
            exports_dir = join(self.recording_dir, "exports")
            if isdir(exports_dir):
                data_exported = True
        except Exception:
            logger.error("No /exports directory found. Export data using Raw Data Exporter plugin")
        return data_exported

    def download_pdf_report(self):
        """
            Saves PDF report into /downloads folder in recording directory.
        """
        if self.any_options_chosen():
            if self.is_data_exported():
                print("\n\nWait for report to be generated...\n\n")
                if not self.data_generated:
                    self.file_handler = FileHandler(self.g_pool)  # set all needed file paths
                    self.load_data_from_csv_files()
                    if isdir(self.file_handler.exports_dir) and isdir(self.file_handler.surfaces_path):  # Fixme
                        self.generate_report()
                        self.plots_dict = {}
            else:
                logger.error("No /exports directory found. Export data using Raw Data Exporter plugin")
        self.data_generated = True

    def generate_report(self):
        if self.language_option == report_pl_opt_label:
            self.properties = properties_pl
        else:
            self.properties = properties

        self.look_for_plots_to_generate()

        report = Report(self.file_handler, self.pdf_report_file_name,
                        self.open_report_after_download_option, self.properties)
        report.add_first_page()
        self.add_plots(report)
        report.save_report()

    def add_plots(self, report):
        fixations_section_added = False
        saccades_section_added = False
        number = 1

        for key_index, plot in self.plots_dict.items():
            print("\n################################################\n"
                  f"## Generate plot \"{plot.title.upper()}\"\n"
                  "################################################\n")
            list_of_plots_options = [
                self.surface_visibility_option,
                self.heatmaps_option,
                self.eye_movements_option,
                self.fixations_per_surface_option,
                self.fixations_frequency_option,
                self.fixations_durations_option,
                # self.saccades_per_surface_option
            ]
            if list_of_plots_options[int(key_index)] is not False:
                if int(key_index) in [3, 4, 5] and not fixations_section_added:
                    report.add_subsection(title=self.properties.fixation_subsection_title,
                                          description=self.properties.fixation_subsection_description)
                    report.add_fixation_report(self.fixation_report)
                    fixations_section_added = True
                if int(key_index) in [6] and not saccades_section_added:
                    report.add_subsection(title=self.properties.saccades_subsection_title,
                                          description=self.properties.saccades_subsection_description)
                    saccades_section_added = True
                plot.set_plot_number(number)
                number += 1
                plot.create()
                report.add_plot(plot)

    def look_for_plots_to_generate(self):
        """
            Checks which plots were chosen to report
            and generates them into /downloads directory as PNG images.
        """

        if self.surface_visibility_option:
            self.plots_dict["0"] = SurfaceVisibilityPlot(
                image_path=join(self.file_handler.images_dir,
                                self.properties.surface_visibility_percentage_filename),
                surfaces_dict=self.surfaces_objects_dict,
                total_gaze_point_count=self.total_gaze_point_count,
                rec_duration=self.duration,
                properties=self.properties)

        if self.heatmaps_option:
            self.plots_dict["1"] = HeatmapPlot(
                image_path=join(self.file_handler.images_dir, self.properties.heatmaps_filename),
                surfaces_dict=self.surfaces_objects_dict,
                properties=self.properties)

        if self.eye_movements_option:
            self.plots_dict["2"] = EyeMovementsPlot(
                image_path=join(self.file_handler.images_dir, self.properties.eye_movements_filename),
                surfaces_dict=self.surfaces_objects_dict,
                properties=self.properties,
                rec_duration=self.duration,
                all_eye_movements=self.all_eye_movement_dict)

        if self.fixations_per_surface_option:
            self.plots_dict["3"] = FixationsPerSurfacePlot(
                image_path=join(self.file_handler.images_dir, self.properties.fixations_count_per_surface_filename),
                surfaces_dict=self.surfaces_objects_dict,
                properties=self.properties)

        if self.fixations_frequency_option:
            self.plots_dict["4"] = FixationsFrequencyPlot(
                image_path=join(self.file_handler.images_dir, self.properties.fixations_frequency_filename),
                surfaces_dict=self.surfaces_objects_dict,
                total_gaze_point_count=self.total_gaze_point_count,
                rec_duration=self.duration,
                fixation_count=self.fixation_report.get_fixation_count(),
                properties=self.properties)

        if self.fixations_durations_option:
            self.plots_dict["5"] = FixationsDurationPlot(
                image_path=join(self.file_handler.images_dir, self.properties.fixations_durations_filename),
                surfaces_dict=self.surfaces_objects_dict,
                rec_start=self.first_timestamp,
                rec_duration=self.duration,
                properties=self.properties)

        # if self.saccades_per_surface_option:
        #     self.plots_dict["6"] = SaccadesPerSurfacePlot(
        #         image_path=join(self.file_handler.images_dir,
        #                                 self.properties.saccades_count_per_surface_filename),
        #         surfaces_dict=self.surfaces_objects_dict,
        #         properties=self.properties)

        print("\nChosen plots:")
        for plot in self.plots_dict.values():
            print("\t- ", plot.title)

    def any_options_chosen(self):
        if True in [
            self.surface_visibility_option,
            self.heatmaps_option,
            self.fixations_per_surface_option,
            self.fixations_frequency_option,
            self.fixations_durations_option
            # , self.saccades_per_surface_option
        ]:
            return True
        else:
            logger.warning("Choose plots which should be added to report!")
            return False

    def load_data_from_csv_files(self):
        if self.file_handler.exports_dir is not None:
            self.recording_info_dict = self.file_handler.load_recording_info()
            self.fixation_report = self.file_handler.load_fixation_report_data()

            # find which surfaces were defined
            self.surfaces_objects_dict, self.total_gaze_point_count = self.file_handler.load_surfaces_gaze_data()

            # load info about eye movements (Eye Movement Detector)
            self.all_eye_movement_dict = self.file_handler.load_eye_movement_by_segment()

            # load info about fixations (Fixation Detector)
            self.file_handler.load_fixations_data_for_each_defined_surface(self.surfaces_objects_dict)
            self.file_handler.load_fixations_data_for_not_defined_surf(self.surfaces_objects_dict)

            # load gaze points used later in creating Heatmaps
            self.file_handler.load_gaze_points_for_each_defined_surface(self.surfaces_objects_dict)

            # self.file_handler.load_numpy_fixations_file()
