class Surface(object):

    def __init__(self, name, gaze_count):
        self.name = name
        self.gaze_count = gaze_count  # gaze points on this surface
        self.fixations_list = []  # from fixations_on_surface_<name>_<timestamp>.csv file without on_srf=False values
        self.gaze_points_list = []  # from gaze_positions_on_surface_<name>_<timestamp>.csv file
        self.normalized_gaze_points_list = []  # from gaze_positions_on_surface_<name>_<timestamp>.csv file
        self.surface_visibility_percent = None
        self.saccades_list = None
        # self.durations_list = []
        # self.x_list = []
        # self.y_list = []

    def to_string(self):
        surface_string = """\nSURFACE '{}'
            gaze_count: {}
            total fixations number: {}
            total fixations duration: {}
            """.format(
            self.get_surface_name(),
            self.get_gaze_count(),
            self.get_total_number_of_fixations(),
            self.get_total_duration_of_fixations())

        return surface_string

    #

    # getters
    #

    def get_surface_name(self):
        return self.name

    def get_gaze_count(self):
        return self.gaze_count

    def get_surface_visibility_percent(self):
        return self.surface_visibility_percent

    def calculate_surface_visibility_percent(self, total_gaze_point_count):
        """
            Calculates how many time (in percent) was spent on looking at this surface.

            gaze_point_count * 100
            ----------------------
            total_gaze_point_count

        :param total_gaze_point_count: number of gaze points in recording
        """
        print("Calculating surface visibility... \ngaze_count = {} and total_gaze_point_count = {}".format(
            self.gaze_count, total_gaze_point_count))

        self.set_surface_visibility_percent(int(self.gaze_count) / int(total_gaze_point_count) * 100)
        surface_visibility_percent = self.get_surface_visibility_percent()
        print("Surface {} was visible over {} % of the whole recording.".format(self.get_surface_name(),
                                                                                surface_visibility_percent))
        return surface_visibility_percent

    def get_fixations_list(self):
        return self.fixations_list

    def get_total_number_of_fixations(self):
        """
            Specifies how many fixations (only with parameter on_srf equals True!) were registered on surface.
            :return: number of fixations that were detected on specific surface
        """
        return len(self.fixations_list)

    def get_total_number_of_saccades(self):
        return len(self.saccades_list)

    def get_gaze_points_list(self):
        return self.gaze_points_list

    def get_total_number_of_gaze_points(self):
        return len(self.gaze_points_list)

    def get_fixations_durations_list(self):
        duration_list = []
        for fixation in self.get_fixations_list():
            duration_list.append(fixation.get_duration())
        return duration_list

    def get_total_duration_of_fixations(self):
        return sum(self.get_fixations_durations_list())

    def get_fixation_x_scaled_list(self):
        x_scaled_list = []
        for fixation in self.get_fixations_list():
            x_scaled_list.append(fixation.get_x_scaled())
        return x_scaled_list

    def get_fixation_y_scaled_list(self):
        y_scaled_list = []
        for fixation in self.get_fixations_list():
            y_scaled_list.append(fixation.get_y_scaled())
        return y_scaled_list

    def get_gaze_points_x_list(self):
        x_list = []
        for gaze_point in self.get_gaze_points_list():
            x_list.append(gaze_point.get_x())
        return x_list

    def get_gaze_points_y_list(self):
        y_list = []
        for gaze_point in self.get_gaze_points_list():
            y_list.append(gaze_point.get_y())
        return y_list

    def get_normalized_gaze_points_x_list(self):
        x_list = []
        for gaze_point in self.normalized_gaze_points_list:
            x_list.append(gaze_point.get_x())
        return x_list

    def get_normalized_gaze_points_y_list(self):
        y_list = []
        for gaze_point in self.normalized_gaze_points_list:
            y_list.append(gaze_point.get_y())
        return y_list

    #
    # setters
    #

    def set_surface_visibility_percent(self, percent):
        self.surface_visibility_percent = percent

    def add_fixation_to_surface_list(self, fixation):
        """
            Adds Fixation instance to list of surface fixations.
            :param fixation: Fixation object
        """
        self.fixations_list.append(fixation)

    def add_gaze_point_to_list(self, point):
        self.gaze_points_list.append(point)

    def add_normalized_gaze_point_to_list(self, point):
        self.normalized_gaze_points_list.append(point)

    def calculate_fixations_frequency(self, recording_duration):
        fixations_on_srf = self.get_total_number_of_fixations()
        time_on_surface = (recording_duration * self.surface_visibility_percent) / 100
        if fixations_on_srf != 0 and time_on_surface != 0:
            frequency = fixations_on_srf / time_on_surface
        else:
            print("""\nWARNING
            Fixations frequency could not be calculated for surface '{}'
            fixations_on_srf = {}
            time_on_surface = {} s
            """.format(self.get_surface_name(), fixations_on_srf, time_on_surface))
            frequency = 0

        print(
            "\nFixations frequency for surface '{}' = {} fixations/s (rounded)".format(self.name, round(frequency, 2)))
        return frequency
