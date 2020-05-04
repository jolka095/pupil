class FixationReport(object):
    """
        Class represents date from fixation_report.csv file.
    """

    def __init__(self, dictionary):
        self.max_dispersion = dictionary["max_dispersion"] if ("max_dispersion" in dictionary) else "NA"
        self.min_duration = dictionary["min_duration"] if ("min_duration" in dictionary) else "NA"
        self.max_duration = dictionary["max_duration"] if ("max_duration" in dictionary) else "NA"
        self.fixation_count = dictionary["fixation_count"] if ("fixation_count" in dictionary) else "NA"

    def to_string(self):
        report = """\nFIXATION REPORT
        max_dispersion:\t{}
        min_duration:\t{}
        max_duration:\t{}
        fixation_count:\t{}""".format(
            self.max_dispersion,
            self.min_duration,
            self.max_duration,
            self.fixation_count
        )
        return report

    def get_fixation_count(self):
        return int(self.fixation_count)
