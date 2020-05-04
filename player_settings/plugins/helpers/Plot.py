import logging
from abc import abstractmethod, ABC

import matplotlib.pyplot as plt
import numpy as np

from player_settings.plugins.helpers.properties.properties import *

logger = logging.getLogger(__name__)


def get_date_from_timestamp(timestamp_str):
    # timestamp_str = 1553531761.37946
    import datetime
    converted_date = datetime.datetime.fromtimestamp(timestamp_str).strftime('%H:%M:%S')
    # converted_date = datetime.utcfromtimestamp(int(float(timestamp_str))).strftime('%Y-%m-%d %H:%M:%S')
    print("start_timestamp: {} converted to {}".format(timestamp_str, converted_date))
    return converted_date


class Plot(ABC):
    def __init__(self, image_path, surfaces_dict):
        self.title = None
        self.description = None
        self.image_path = image_path
        self.surfaces_dict = surfaces_dict
        self.colors = ['red', 'yellow', 'green', 'blue', 'pink']

    @abstractmethod
    def create(self):
        pass

    def save_as_image(self, plot, fig):
        plot.title(self.title, fontsize=16, pad=20)
        plot.margins(0.2)
        # plt.subplots_adjust(top=0.2)
        plot.tight_layout()

        if fig is not None:
            fig.savefig(self.image_path)
        else:
            logger.error("Error during plot creation ({})".format(self.title))


class SurfaceVisibilityPlot(Plot):
    """
        Generates plot which shows how much time was spent looking on each surface.
    """
    sizes = []
    defined_surfaces_gaze_percent = 0
    explode_tuple = None

    def __init__(self, image_path, surfaces_dict, total_gaze_point_count):
        super().__init__(image_path, surfaces_dict)
        self.title = surface_visibility_plot_title
        self.description = surface_visibility_percentage_description

        self.total_gaze_point_count = total_gaze_point_count
        self.labels = list(self.surfaces_dict.keys())

    def get_explode_tuple_for_plot(self):
        """
            Returns tuple with values 0 or 0.1.
            Value 0.1 is for the (last) part of plot which is distinguished.
        """
        print("\ngetting explode list...")
        explode_list = []
        for i, el in enumerate(self.labels):
            print(el)
            explode_list.append(0)
            if i == (len(self.labels) - 1):
                explode_list[i] = 0.1
        print(tuple(explode_list))
        return tuple(explode_list)

    def create(self):
        """
            :return: figure (saved in /downloads directory as PNG image) with proper plot
        """
        not_found_param_not_on_any_surface = True

        print("\n\nSurfaces visibility (%)")
        if len(self.sizes) == 0:
            for surface_name, surface_obj in self.surfaces_dict.items():
                if surface_name in "not_on_any_surface":
                    not_found_param_not_on_any_surface = False
                percent = surface_obj.calculate_surface_visibility_percent(self.total_gaze_point_count)
                self.defined_surfaces_gaze_percent += percent
                self.sizes.append(percent)
                print(surface_name, "\t\t->", round(percent, 2), "%")

            # if parameter "not_on_any_surface" is not specified in surfaces_gaze_distribution.csv
            if not_found_param_not_on_any_surface:
                if "inne" not in self.labels:
                    self.labels.append("inne")
                other_surfaces_gaze_percent = 100 - self.defined_surfaces_gaze_percent
                self.sizes.append(other_surfaces_gaze_percent)
                print("other_surfaces_gaze_percent", round(other_surfaces_gaze_percent, 2))
        elif "inne" not in self.labels and "not_on_any_surface" not in self.labels:
            self.labels.append("inne")
        else:
            print("Data already calculated.")

        self.explode_tuple = self.get_explode_tuple_for_plot()
        # print("****EXPLODE ", self.explode_tuple, "****labels ", self.labels, "****sizes ", self.sizes)

        # making plot
        #
        fig, ax1 = plt.subplots()
        patches, texts, autotexts = ax1.pie(self.sizes, autopct='%1.1f%%', startangle=90, explode=self.explode_tuple)
        plt.setp(autotexts, size='x-small')
        plt.legend(patches, self.labels, loc="best")
        plt.axis('equal')

        self.save_as_image(plt, fig)
        return fig


class FixationsPerSurfacePlot(Plot):

    def __init__(self, image_path, surfaces_dict):
        super().__init__(image_path, surfaces_dict)
        self.title = fixations_count_per_surface_plot_title
        self.description = fixations_count_per_surface_description

        self.labels = list(self.surfaces_dict.keys())

    def autolabel(self, ax, rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0, 'right': 1, 'left': -1}

        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(offset[xpos] * 3, 3),  # use 3 points offset
                        textcoords="offset points",  # in both directions
                        ha=ha[xpos], va='bottom')

    def create(self):
        fixation_count_list = []  # liczba fiksacji dla każdej powierzchni
        fixation_durations_sum_list = []  # czas trwania fiksacji zsumowany per kazda powierzchnia

        for surface_name, surface_obj in self.surfaces_dict.items():
            number_of_fixations = surface_obj.get_total_number_of_fixations()
            fixation_count_list.append(number_of_fixations)

            sum_of_fixations_durations = surface_obj.get_total_duration_of_fixations()
            rounded_total_fixation_durations = round(sum_of_fixations_durations / 1000, 2)  # convert from ms to s
            fixation_durations_sum_list.append(rounded_total_fixation_durations)
            print(surface_obj.to_string())

            # total_fixation_durations = 0

            # if surface_name not in "not_on_any_surface":  # if surface is one of defined ones
            #     fixation_count_list.append(surface_obj.get_total_number_of_fixations())
            #     for fixation in surface_obj.get_fixations_list():
            #         total_fixation_durations += fixation.get_duration()
            #     print("\ttotal_fixation_durations: ", total_fixation_durations)
            #     rounded_total_fixation_durations = round(total_fixation_durations / 1000, 2)  # convert from ms to s
            #     fixation_durations_sum_list.append(rounded_total_fixation_durations)
#             # else:
#             #     self.labels.remove(surface_name)

        # making plot
        #
        print("fixation_count_list")
        print(fixation_count_list)
        ind = np.arange(len(fixation_count_list))  # the x locations for the groups
        width = 0.3  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind - width / 2, fixation_count_list, width,
                        label=number_of_fixations_label.format(sum(fixation_count_list)))
        rects2 = ax.bar(ind + width / 2, fixation_durations_sum_list, width,
                        label=fixations_durations_axis_label)

        # plt.xlabel(surface_name_label, fontsize=14)
        ax.set_xticks(ind)
        ax.set_xticklabels(self.labels, rotation="-20", fontsize=8)
        ax.legend(loc='upper right', prop={'size': 8})

        self.autolabel(ax, rects1, "left")
        self.autolabel(ax, rects2, "right")

        self.save_as_image(plt, fig)
        return fig


# TODO
class FixationsFrequencyPlot(Plot):

    def __init__(self, image_path, surfaces_dict, rec_duration, fixation_count):
        super().__init__(image_path, surfaces_dict)
        self.title = fixations_frequency_plot_title
        self.description = fixations_frequency_description

        self.labels = list(self.surfaces_dict.keys())
        self.labels.insert(0, "Średnia")
        self.recording_duration = rec_duration
        general_frequency = fixation_count / rec_duration  # fixations/second
        self.fixations_frequency_list = [general_frequency]

    def create(self):
        for surface_name, surface_obj in self.surfaces_dict.items():
            self.fixations_frequency_list.append(surface_obj.calculate_fixations_frequency(self.recording_duration))
        # print("FIXATIONS FREQUENCIES {}".format(self.fixations_frequency_list))

        # making plot
        #
        ind = np.arange(len(self.fixations_frequency_list))  # the x locations for the groups
        fig, ax = plt.subplots()
        bar_list = ax.bar(ind, self.fixations_frequency_list)
        bar_list[0].set_color('g')
        ax.set_xticks(ind)
        ax.set_xticklabels(self.labels, rotation="-20")
        plt.ylabel(number_of_fixations_per_second_label)
        ax.grid(True)

        self.save_as_image(plt, fig)
        return fig


# TODO
class FixationsDurationPlot(Plot):

    def __init__(self, image_path, surfaces_dict):
        super().__init__(image_path, surfaces_dict)
        self.title = fixations_durations_plot_title
        self.description = fixations_durations_description

        self.labels = list(self.surfaces_dict.keys())

    def create(self):

        color_index = 0
        num = 0.1
        ytick = num
        bar_height = num
        gap = bar_height + num

        xranges_tuples_list = []
        all_timestamps = []
        min_timestamps = []
        max_timestamps = []
        yticks = []

        # making plot
        #
        fig, ax = plt.subplots()

        for surface_name, surface_obj in self.surfaces_dict.items():
            yticks.append(ytick)

            for i, fixation in enumerate(surface_obj.get_fixations_list()):
                timestamp = fixation.get_start_timestamp()
                duration = fixation.get_duration()

                if timestamp is not None and timestamp is not "":
                    all_timestamps.append(timestamp)
                if i == 0:
                    min_timestamps.append(timestamp)
                if i == int(surface_obj.get_total_number_of_fixations()) - 1:
                    max_timestamps.append(timestamp)

                tmp_tuple = (timestamp, duration)
                xranges_tuples_list.append(tmp_tuple)

            # print("xrange for surface {}: \n{}".format(surface_name, xranges_tuples_list))

            ax.broken_barh(xranges=xranges_tuples_list, yrange=(ytick, bar_height), facecolors=self.colors[color_index])
            color_index += 1
            ytick += gap
            xranges_tuples_list = []

        # X AXIS
        get_date_from_timestamp(min(min_timestamps))
        get_date_from_timestamp(max(max_timestamps))
        ax.set_xlim(left=min(min_timestamps), right=max(max_timestamps))
        ax.set_xticklabels(all_timestamps, rotation="-90")
        ax.set_xlabel("Czas")

        # Y AXIS
        ax.set_ylim(bottom=0, top=max(yticks) + num * 2)  # OK
        new_yticks = []
        for i, ytick in enumerate(yticks):
            new_yticks.append(ytick + num / 2)
        ax.set_yticks(new_yticks)  # OK
        ax.set_yticklabels(self.labels)  # OK

        ax.grid(True)

        self.save_as_image(plt, fig)
        return fig


# TODO
class SaccadesPerSurfacePlot(Plot):

    def __init__(self, image_path, surfaces_dict):
        super().__init__(image_path, surfaces_dict)
        self.title = saccades_count_per_surface_plot_title
        self.description = saccades_count_per_surface_description

    def create(self):
        # making plot
        #
        fig, ax = plt.subplots()

        self.save_as_image(plt, fig)
        return fig


# TODO
class Heatmap(Plot):

    def __init__(self, image_path, surfaces_dict):
        super().__init__(image_path, surfaces_dict)
        self.title = None
        self.description = None

    def create(self):
        labels = list(self.surfaces_dict.keys())

        fig, axs = plt.subplots(nrows=len(labels), figsize=(6, 9))
        fig.suptitle(self.title, fontsize=16)

        for i, surface_name in enumerate(labels):
            if surface_name != "not_on_any_surface":
                print("Adding surface {}".format(surface_name))
                xs = self.surfaces_dict[surface_name].get_fixation_x_scaled_list()
                ys = self.surfaces_dict[surface_name].get_fixation_y_scaled_list()
                print(xs)
                print(ys)
                # axs[i].hist2d(xs, ys, bins=20)
                axs[i].imshow([xs, ys], interpolation='hermite', cmap='viridis')

        # plt.hist2d(xs, ys, bins=10)
        # plt.hist2d(xs, ys, bins=100)

        # making plot
        #
        # heatmap, xedges, yedges = np.histogram2d(xs, ys, bins=100)
        # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        #
        # plt.clf()
        # plt.imshow(heatmap.T, extent=extent, origin='lower')

        self.save_as_image(plt, fig)
        return fig
