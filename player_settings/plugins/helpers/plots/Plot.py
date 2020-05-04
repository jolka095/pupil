import logging
from abc import abstractmethod, ABC
import numpy as np
from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)


class Plot(ABC):
    plot_number = None

    def __init__(self, image_path, surfaces_dict, properties):
        self.title = None
        self.description = None
        self.image_path = image_path
        self.surfaces_dict = surfaces_dict
        self.properties = properties
        self.colors = ['blue', 'green', 'red', 'purple', 'coral', 'brown', 'cyan', 'magenta', 'yellow', 'pink',
                       'gold', 'lime', 'chocolate', 'crimson']
        self.np = np
        self.plt = plt
        self.fontsize = 14

    @abstractmethod
    def create(self):
        pass

    def autolabel(self, ax, rects):
        for rect in rects:
            height = rect.get_height()

            ax.text(rect.get_x() + rect.get_width() / 2., 1.02 * height,
                    '{}'.format(height),
                    ha='center', va='bottom')

    def save_as_image(self, plot, fig):
        if "Heatmaps" in self.title or "Mapy cieplne" in self.title:
            plot.suptitle(self.title, fontsize=16)
        else:
            plot.title(self.title, fontsize=16, pad=20)
            plot.tight_layout()

        if fig is not None:
            fig.savefig(self.image_path)
        else:
            logger.error("Error during plot creation ({})".format(self.title))

    def calculate_x_tick_labels(self, rec_duration, start_timestamp):
        global time_gap
        x_ticks = [start_timestamp]
        x_tick_labels = [0]
        time_unit = "min"
        seconds = False

        if 0 < rec_duration <= (2 * 60):
            time_gap = 5
            seconds = True
            time_unit = "s"
        if (2 * 60) < rec_duration <= (5 * 60):
            time_gap = 20
        if (5 * 60) < rec_duration <= (10 * 60):
            time_gap = 30
        if (10 * 60) < rec_duration <= (20 * 60):
            time_gap = 60
        if rec_duration > (20 * 60):
            time_gap = (5 * 60)

        print("\n\nRECORDING DURATION {}s".format(rec_duration))
        print("START TIMESTAMP {}s".format(start_timestamp))
        print("TIME GAP {}s".format(time_gap))
        tmp_label = 0
        for i in range(rec_duration):
            if i % time_gap == 0:
                tmp_timestamp = start_timestamp + time_gap
                tmp_label += time_gap

                x_ticks.append(tmp_timestamp)
                if seconds:
                    x_tick_labels.append(tmp_label)
                else:
                    x_tick_labels.append(int(tmp_label / 60))
                start_timestamp = tmp_timestamp
        return x_ticks, x_tick_labels, time_unit

    def set_plot_number(self, number):
        self.plot_number = number
        self.title = "[{}] {}".format(number, self.title)
