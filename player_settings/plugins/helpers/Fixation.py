class Fixation(object):

    def __get_parameter_from_dict__(self, dictionary, key):
        return dictionary[key] if (key in dictionary) else "NA"

    def __init__(self, dictionary):
        self.id = self.__get_parameter_from_dict__(dictionary, "id")

        # Timestamp of the first related gaze datum
        self.start_timestamp = self.__get_parameter_from_dict__(dictionary, "start_timestamp")

        # Exact fixation duration, in milliseconds
        self.duration = self.__get_parameter_from_dict__(dictionary, "duration")

        # Position of the fixation’s centroid
        self.x_scaled = self.__get_parameter_from_dict__(dictionary, "x_scaled")
        self.y_scaled = self.__get_parameter_from_dict__(dictionary, "y_scaled")

        # only fixations with "on_srf = True" are loaded
        self.on_srf = self.__get_parameter_from_dict__(dictionary, "on_srf")

    def to_string(self):
        fixation = """\nFIXATION #{}
        start_timestamp: {}
        duration: {}
        x_scaled: {}
        y_scaled: {}
        on_srf: {}""".format(
            self.id,
            self.start_timestamp,
            self.duration,
            self.x_scaled,
            self.y_scaled,
            self.on_srf
        )
        return fixation

    def get_id(self):
        return self.id

    def get_start_timestamp(self):
        return float(self.start_timestamp)

    def get_duration(self):
        return float(self.duration)

    def get_x_scaled(self):
        return float(self.x_scaled)

    def get_y_scaled(self):
        return float(self.y_scaled)
