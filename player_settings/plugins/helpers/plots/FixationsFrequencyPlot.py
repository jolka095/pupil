from player_settings.plugins.helpers.plots.Plot import Plot


class FixationsFrequencyPlot(Plot):

    def __init__(self, image_path, surfaces_dict, total_gaze_point_count, rec_duration, fixation_count, properties):
        super().__init__(image_path, surfaces_dict, properties)
        self.title = self.properties.fixations_frequency_plot_title
        self.description = self.properties.fixations_frequency_description

        self.labels = list(self.surfaces_dict.keys())
        self.labels.insert(0, "średnia")
        self.total_gaze_point_count = total_gaze_point_count
        self.recording_duration = rec_duration
        general_frequency = fixation_count / rec_duration  # fixations/second
        self.fixations_frequency_list = [general_frequency]

    def create(self):
        for surface_name, surface_obj in self.surfaces_dict.items():
            if surface_obj.get_surface_visibility_percent() is None:
                surface_obj.calculate_surface_visibility_percent(self.total_gaze_point_count)

            self.fixations_frequency_list.append(surface_obj.calculate_fixations_frequency(self.recording_duration))
        # print("FIXATIONS FREQUENCIES {}".format(self.fixations_frequency_list))

        fig, ax = self.plt.subplots()
        x_ticks = self.np.arange(len(self.fixations_frequency_list))  # the x locations for the groups

        bar_list = ax.bar(x_ticks, [round(elem, 2) for elem in self.fixations_frequency_list])

        bar_list[0].set_color('g')
        bar_list[len(bar_list) - 1].set_color('grey')

        ax.set_xticks(x_ticks)
        self.labels[len(self.labels) - 1] = 'inne'
        ax.set_xticklabels(self.labels, rotation="-20")

        self.plt.ylabel(self.properties.number_of_fixations_per_second_label)
        # ax.grid(True)
        self.autolabel(ax, bar_list)
        self.plt.margins(0.1)
        self.save_as_image(self.plt, fig)
        return fig
