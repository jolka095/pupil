from player_settings.plugins.helpers.plots.Plot import Plot


class FixationsPerSurfacePlot(Plot):

    def __init__(self, image_path, surfaces_dict, properties):
        super().__init__(image_path, surfaces_dict, properties)
        self.title = properties.fixations_count_per_surface_plot_title
        self.description = properties.fixations_count_per_surface_description

        self.labels = list(self.surfaces_dict.keys())

    def create(self):
        bar_width = 0.4
        fixation_count_list = []  # liczba fiksacji dla każdej powierzchni
        fixation_durations_sum_list = []  # czas trwania fiksacji zsumowany per kazda powierzchnia
        for surface_name, surface_obj in self.surfaces_dict.items():
            number_of_fixations = surface_obj.get_total_number_of_fixations()
            fixation_count_list.append(number_of_fixations)

            sum_of_fixations_durations = surface_obj.get_total_duration_of_fixations()
            rounded_total_fixation_durations = round(sum_of_fixations_durations / 1000, 2)  # convert from ms to s
            fixation_durations_sum_list.append(rounded_total_fixation_durations)
            print(surface_obj.to_string())

        fig, ax = self.plt.subplots()
        x_ticks = self.np.arange(len(fixation_count_list))  # the x locations for the groups

        fixation_count_bar = ax.bar(x_ticks - bar_width / 2, fixation_count_list, bar_width,
                                    label=self.properties.number_of_fixations_label.format(sum(fixation_count_list)))
        fixation_duration_bar = ax.bar(x_ticks + bar_width / 2, fixation_durations_sum_list, bar_width,
                                       label=self.properties.fixations_durations_axis_label)

        ax.set_xticks(x_ticks)
        self.labels[len(self.labels) - 1] = 'inne'
        ax.set_xticklabels(self.labels, rotation="-20", fontsize=8)
        ax.legend(loc='upper right', prop={'size': 8}, ncol=2)

        self.autolabel(ax, fixation_count_bar)
        self.autolabel(ax, fixation_duration_bar)

        self.plt.margins(0.2)
        self.save_as_image(self.plt, fig)
        return fig
