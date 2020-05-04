from player_settings.plugins.helpers.plots.Plot import Plot


class FixationsDurationPlot(Plot):

    def __init__(self, image_path, surfaces_dict, rec_start, rec_duration, properties):
        super().__init__(image_path, surfaces_dict, properties)
        self.title = self.properties.fixations_durations_plot_title
        self.description = self.properties.fixations_durations_description
        self.labels = list(self.surfaces_dict.keys())
        self.start_timestamp_synced = rec_start  # g_pool.timestamps[0]
        self.recording_duration_time = int(rec_duration)

        print("start_timestamp_synced {} \nrecording_duration_time {}".format(rec_start, int(rec_duration)))

    def create(self):
        color_index = 0  # TODO: maybe change to random index
        num = 0.1
        ytick = num
        bar_height = num
        gap = bar_height + num

        yticks = []  # for yrange (yrange : (ymin, yheight))
        xranges_tuples_list = []  # (xmin, xwidth)

        fig, ax = self.plt.subplots()
        for surface_name, surface_obj in self.surfaces_dict.items():
            yticks.append(ytick)
            for i, fixation in enumerate(surface_obj.get_fixations_list()):
                tmp_tuple = (fixation.get_start_timestamp(), fixation.get_duration() / 1000)
                xranges_tuples_list.append(tmp_tuple)

            ax.broken_barh(xranges_tuples_list, yrange=(ytick, bar_height), facecolors=self.colors[color_index])

            color_index += 1
            ytick += gap
            xranges_tuples_list = []

        # X AXIS
        right_limit = (self.start_timestamp_synced + self.recording_duration_time)
        ax.set_xlim(left=self.start_timestamp_synced, right=right_limit)
        x_ticks, x_tick_labels, time_unit = self.calculate_x_tick_labels(
            rec_duration=self.recording_duration_time,
            start_timestamp=self.start_timestamp_synced)  # align x_ticks

        # TODO: odkomentować jeśli wykres ma się kończyć dokładnie tam gdzie koniec nagrania
        # x_ticks[len(x_ticks) - 1] = right_limit
        # x_tick_labels[len(x_tick_labels) - 1] = int(x_tick_labels[len(x_tick_labels) - 2] + right_limit - x_ticks[len(x_ticks) - 2])

        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_tick_labels, fontsize=8)
        ax.set_xlabel(self.properties.recording_time_label.format(time_unit))

        # Y AXIS
        ax.set_ylim(bottom=0, top=max(yticks) + num * 2)
        y_ticks_labels = list(map(lambda y_tick: y_tick + num / 2, yticks))  # align y_ticks
        ax.set_yticks(y_ticks_labels)
        self.labels[len(self.labels) - 1] = 'inne'  # give different name instead of "not_on_any_surface"
        ax.set_yticklabels(self.labels)

        ax.grid(True)
        self.save_as_image(self.plt, fig)
        return fig
