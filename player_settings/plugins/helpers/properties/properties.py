# report info

pdf_report_file_name = "pupil_report_{}.pdf"
report_title = "Eye-tracking data analysis"
report_subtitle = "Report with plots and figures"
subtitle_with_date = "Generated date: {}"
subtitle_with_rec_dir_path = "Recording directory: {}"
subtitle_with_exported_dir_path = "Exports subdirectory: {}"

# subsections
fixation_subsection_title = "Fixations"
fixation_subsection_description = \
    "\n      Fixations are eye movements that stabilize the retina over a stationary object of interest. " \
    "The term \"fixation\" is used to refer to the point of focus on particular area in field of view. " \
    "Fixation is the point between any two saccades, during which the eyes are " \
    "relatively stationary and virtually all visual input occurs. " \
    "They are characterized by the miniature eye movements: tremor, drift, and microsaccades. " \
    "\n\n    There are many methods to detect fixations and saccades. Pupil software uses dispersion-threshold " \
    "identification algorithm (I-DT) which identifies fixations as groups of consecutive points within a particular " \
    "dispersion, or maximum separation. Because fixations typically have a duration of at least 100 ms, " \
    "dispersion-based identification techniques often incorporate a minimum duration threshold " \
    "of 100-200 ms to help alleviate equipment variability. (D. Salvucci & J. Goldberg, 2000)."
fixation_detector_table_description = "\n\n      Fixation Detector settings in Pupil Capture " \
                                      "and total number of fixations in recording: "
fixation_detector_settings_values_param = "PARAMETER"
fixation_detector_settings_values_val = "VALUE"

saccades_subsection_title = "Saccades"
saccades_subsection_description = \
    "\n      Saccades are rapid eye movements used in repositioning the fovea to a new location " \
    "in the visual environment. In that moment brain decides which element will be focused, i.e. " \
    "where the next fixation will occur. Saccadic movements are both voluntary and reflexive. " \
    "Saccades range in duration from 10 to 100 ms, which is a sufficiently " \
    "short duration to render the executor effectively blind during the transition."

not_defined_area = "not_on_any_surface"

# descriptions for plots in report

#########################################################
#       Surface visibility
#########################################################

surface_visibility_plot_title = "Surfaces visibility"
surface_visibility_percentage_description = \
    "\n      This plot shows how many time user was looking at particular surface, which was defined previously. " \
    "Eye-tracking data on the basis of which plot was made, were taken from file called " \
    "\"surface_gaze_distribution.csv\". That file contains information about number of gaze points " \
    "on particular areas (surfaces) and about " \
    "total number of gaze points in whole recording (\"total_gaze_point_count\" parameter)."
surface_visibility_percentage_filename = "surface_visibility_percentage.png"  # image file (i.e. plot, chart or diagram)

#########################################################
#       Fixations per surface
#########################################################

fixations_count_per_surface_plot_title = "Fixations on surfaces"
fixations_count_per_surface_description = \
    "      This plot shows number of fixation on particular surfaces and their duration." \
    " Data from files with \"fixations_on_surface\" prefix were used to generate this plot. These files contains " \
    "parameters like:  " \
    "\n- id (identification number)" \
    "\n- start_timestamp (start of fixation)" \
    "\n- duration (fixation duration [ms])" \
    "\n- on_srf (determines whether fixation was detecter on surface or not) " \
    "\nATTENTION: Only fixations with parameter \"on_srf\" equal True were taken into account. " \
    "In some cases, this parameter has the same value for more than one surface " \
    "that is why some discrepancies in total number of fixations can occur."
fixations_count_per_surface_filename = "fixations_count_per_surface.png"

#########################################################
#       Fixations frequency
#########################################################

fixations_frequency_plot_title = "Fixations frequency"
fixations_frequency_description = \
    "\n      Plot shows fixation frequencies on particular surfaces. " \
    "Average frequency is equal to quotient of: " \
    "\n- number of all fixations " \
    "\n- and total duration of recording." \
    "\nOn the other hand, frequency of fixations on particular area is equal to quotient of:" \
    "\n- number of fixations on this surface" \
    "\n- and time spent on looking at this area." \
    "\nData from files named \"surface_gaze_distribution.csv\" and with prefix " \
    "\"fixations_on_surface\" were used to create this plot."
fixations_frequency_filename = "fixations_frequency.png"

#########################################################
#       Fixations durations
#########################################################

fixations_durations_plot_title = "Fixations on timeline"
fixations_durations_description = \
    "\n      This plot shows fixations on timeline. " \
    "Data from files named \"info.csv\" and with prefix " \
    "\"fixations_on_surface\" were used to create this plot." \
    "\n\nParameters which were use to calculation are:" \
    "\n- \"start_timestamp\" (start of every fixation)," \
    "\n- \"duration\" (duration of particular fixations)," \
    "\n- \"Start Time (Synced)\" (recording start timestamp)," \
    "\n- \"Duration Time\" (recording duration)."
fixations_durations_filename = "fixations_durations.png"

#########################################################
#       Saccades count
#########################################################

saccades_count_per_surface_plot_title = "Saccades on surfaces"
saccades_count_per_surface_description = \
    "\n      Saccades count - test plot description. Lorem ipsum dolor sit amet, "
saccades_count_per_surface_filename = "saccades_count_per_surface.png"

#########################################################
#       Heatmaps
#########################################################

heatmaps_plot_title = "Heatmaps"
heatmaps_description = \
    "\n      Heatmaps visualizes the distribution of gaze points that lie within each surface. " \
    "Lighter colors represents areas where the amount of time spend gazing on this region was the biggest " \
    "(i.e. there were more gaze points registered in this region). " \
    "Dark places on map are areas avoided by person's gaze."
heatmaps_filename = "heatmaps.png"

#########################################################
#       Eye Movements
#########################################################

eye_movements_title = "Eye movements"
eye_movements_description = \
    "\n      There are many kinds of human eye movement. In Pupil software Eye Movement Detector plugin " \
    "classifies four of them: " \
    "\n- fixation, " \
    "\n- saccade, " \
    "\n- post-saccadic oscillation (PSO)," \
    "\n- smooth pursuit. " \
    "\n      Eye-tracking data on the basis of which plot was made, were taken from file called" \
    " \"eye_movement_by_segment.csv\". The total number of fixations differs remarkably comparing to " \
    "file \"fixation_report.csv\" because different algorithms were used in both plugins."  # TODO
eye_movements_filename = "eye_movements_count_and_duration.png"
eye_movements_list = ["fixations", "saccades", "PSO", "smooth pursuits"]

#########################################################
#       plots properties
#########################################################
number_of_movements_label = "Eye movement count ({})"
number_of_fixations_label = "Fixations count ({})"
number_of_saccades_label = "Saccades count ({})"
movements_durations_axis_label = "Eye movement duration [sec]"
fixations_durations_axis_label = "Fixations duration [sec]"
saccades_durations_axis_label = "Saccades duration [sec]"
surface_name_label = "Surface"
number_of_fixations_per_second_label = "Fixations count per second"
recording_time_label = "Time [{}]"
