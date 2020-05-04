class BasicEyeMovement(object):
    @staticmethod
    def __get_param__(dictionary, key):
        return dictionary[key] if (key in dictionary) else "NA"

    def __init__(self, dictionary):
        self.id = self.__get_param__(dictionary, "id")
        # self.base_type = self.__get_parameter_from_dict__(dictionary, "base_type")
        # self.segment_class = self.__get_parameter_from_dict__(dictionary, "segment_class")
        self.start_frame_index = self.__get_param__(dictionary, "start_frame_index")
        self.end_frame_index = self.__get_param__(dictionary, "end_frame_index")
        self.start_timestamp = self.__get_param__(dictionary, "start_timestamp")  # t. of the 1st related gaze datum
        self.end_timestamp = self.__get_param__(dictionary, "end_timestamp")
        self.duration = self.__get_param__(dictionary, "duration")  # Exact fixation duration, in milliseconds
        self.confidence = self.__get_param__(dictionary, "confidence")
        self.norm_pos_x = self.__get_param__(dictionary, "norm_pos_x")
        self.norm_pos_y = self.__get_param__(dictionary, "norm_pos_y")
        self.gaze_point_3d_x = self.__get_param__(dictionary, "gaze_point_3d_x")
        self.gaze_point_3d_y = self.__get_param__(dictionary, "gaze_point_3d_y")
        self.gaze_point_3d_z = self.__get_param__(dictionary, "gaze_point_3d_z")

    def get_id(self):
        return self.id

    def get_start_timestamp(self):
        return float(self.start_timestamp)

    def get_duration(self):
        return float(self.duration)

    def get_norm_pos_x(self):
        return float(self.norm_pos_x)

    def get_norm_pos_y(self):
        return float(self.norm_pos_y)

    def to_string(self):
        return """#{}
        start_timestamp: {}
        duration: {}
        norm_pos_x: {}
        norm_pos_y: {}
        """.format(self.id, self.start_timestamp, self.duration, self.norm_pos_x, self.norm_pos_y)
