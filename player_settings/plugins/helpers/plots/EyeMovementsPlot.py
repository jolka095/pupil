from player_settings.plugins.helpers.plots.Plot import Plot


class EyeMovementsPlot(Plot):

    def __init__(self, image_path, surfaces_dict, properties, rec_duration, all_eye_movements):
        super().__init__(image_path, surfaces_dict, properties)
        self.title = properties.eye_movements_title
        self.description = properties.eye_movements_description
        self.rec_duration = rec_duration
        self.all_eye_movements = all_eye_movements
        self.labels = list(all_eye_movements.keys())
        self.labels2 = properties.eye_movements_list

    def create(self):
        if len(self.all_eye_movements) > 0:

            bar_width = 0.4

            count_list = []  # how many of each movements
            durations_sum_list = []  # total durations of each eye movement

            for movement_name, movement_obj_list in self.all_eye_movements.items():
                count_list.append(len(movement_obj_list))
                tmp_duration = 0
                for movement in movement_obj_list:
                    tmp_duration += movement.get_duration()
                durations_sum_list.append(round(tmp_duration / 1000, 2))  # convert from ms to s

            # TODO all record or sum of all durations
            # rounded_total_durations = round(self.rec_duration / 1000, 2)  # convert from ms to s

            fig, ax = self.plt.subplots()
            x_ticks = self.np.arange(len(count_list))  # the x locations for the groups

            count_bar = ax.bar(x_ticks - bar_width / 2, count_list, bar_width,
                               label=self.properties.number_of_movements_label.format(sum(count_list)),
                               color=self.colors[3])
            duration_bar = ax.bar(x_ticks + bar_width / 2, durations_sum_list, bar_width,
                                  label=self.properties.movements_durations_axis_label,
                                  color=self.colors[4])

            ax.set_xticks(x_ticks)
            # self.labels[len(self.labels) - 1] = 'inne'
            self.labels = self.labels2
            ax.set_xticklabels(self.labels, rotation="-20", fontsize=8)
            ax.legend(loc='upper right', prop={'size': 8}, ncol=2)

            self.autolabel(ax, count_bar)
            self.autolabel(ax, duration_bar)

            self.plt.margins(0.2)
            self.save_as_image(self.plt, fig)
            return fig
