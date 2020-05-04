from player_settings.plugins.helpers.plots.Plot import Plot


# todo
class SaccadesPerSurfacePlot(Plot):

    def __init__(self, image_path, surfaces_dict, properties):
        super().__init__(image_path, surfaces_dict, properties)
        self.title = self.properties.saccades_count_per_surface_plot_title
        self.description = self.properties.saccades_count_per_surface_description

        self.labels = list(self.surfaces_dict.keys())

    def create(self):
        # bar_width = 0.3
        # count_list = []  # liczba sakad dla każdej powierzchni
        # durations_sum_list = []  # długość sakad zsumowana per kazda powierzchnia
        #
        # for surface_name, surface_obj in self.surfaces_dict.items():
        #     count_list.append(surface_obj.get_total_number_of_saccades())
        #
        #     sum_of_durations = surface_obj.get_total_duration_of_saccades()
        #     rounded_total_durations = round(sum_of_durations / 1000, 2)  # convert from ms to s
        #     durations_sum_list.append(rounded_total_durations)
        #     print(surface_obj.to_string())
        #
        fig, ax = self.plt.subplots()
        # x_ticks = self.np.arange(len(count_list))  # the x locations for the groups
        #
        # fixation_count_bar = ax.bar(x_ticks - bar_width / 2, count_list, bar_width,
        #                             label=self.properties.number_of_saccades_label.format(sum(count_list)))
        # fixation_duration_bar = ax.bar(x_ticks + bar_width / 2, durations_sum_list, bar_width,
        #                                label=self.properties.saccades_durations_axis_label)
        #
        # ax.set_xticks(x_ticks)
        # self.labels[len(self.labels) - 1] = 'inne'
        # ax.set_xticklabels(self.labels, rotation="-20", fontsize=8)
        # ax.legend(loc='upper right', prop={'size': 8}, ncol=2)
        #
        # self.autolabel(ax, fixation_count_bar, "left")
        # self.autolabel(ax, fixation_duration_bar, "right")

        self.plt.margins(0.2)
        self.save_as_image(self.plt, fig)
        return fig
