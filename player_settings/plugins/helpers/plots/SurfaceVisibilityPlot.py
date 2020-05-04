from player_settings.plugins.helpers.plots.Plot import Plot
from player_settings.plugins.helpers.properties.properties import not_defined_area


class SurfaceVisibilityPlot(Plot):
    """
        Generates plot which shows how much time was spent looking on each surface.
    """
    sizes = []
    defined_surfaces_gaze_percent = 0

    def __init__(self, image_path, surfaces_dict, properties, total_gaze_point_count, rec_duration):
        super().__init__(image_path, surfaces_dict, properties)
        self.title = properties.surface_visibility_plot_title
        self.description = properties.surface_visibility_percentage_description
        self.recording_duration = rec_duration  # in [s]

        self.total_gaze_point_count = total_gaze_point_count
        self.labels = list(self.surfaces_dict.keys())  # with or without "not_on_any_surface" key (depends on version)
        self.explode_list = [0.0] * len(self.labels)
        self.explode_list[len(self.labels) - 1] = 0.1
        self.explode_tuple = tuple(self.explode_list)

    def create(self):
        """
            :return: figure (saved in /downloads directory as PNG image) with proper plot
        """
        not_found_param_not_on_any_surface = True

        print("\n\nSurfaces visibility (%)\n\n")
        if len(self.sizes) == 0:
            for surface_name, surface_obj in self.surfaces_dict.items():
                if surface_name in not_defined_area:
                    not_found_param_not_on_any_surface = False
                percent = surface_obj.calculate_surface_visibility_percent(self.total_gaze_point_count)
                self.defined_surfaces_gaze_percent += percent
                self.sizes.append(percent)
                print("\t{}\t->{}%".format(surface_name, round(percent, 2)))

            # if parameter "not_on_any_surface" is not specified in surfaces_gaze_distribution.csv
            if not_found_param_not_on_any_surface:
                if "inne" not in self.labels:
                    self.labels.append("inne")
                other_surfaces_gaze_percent = 100 - self.defined_surfaces_gaze_percent
                self.sizes.append(other_surfaces_gaze_percent)
                print("\t{}\t->{}%".format("other_surfaces_gaze_percent", round(other_surfaces_gaze_percent, 2)))

        elif ("inne" not in self.labels) and (not_defined_area not in self.labels):
            self.labels.append("inne")
        else:
            print("Data already calculated.")

        fig, ax1 = self.plt.subplots()
        patches, texts, autotexts = ax1.pie(self.sizes, autopct='%1.2f%%', startangle=90, explode=self.explode_tuple)
        self.plt.setp(autotexts, size='x-small')

        self.labels[len(self.labels) - 1] = 'inne'
        self.plt.legend(patches, self.labels, loc="best")
        self.plt.axis('equal')
        ax1.text(-1.8, -1.2, '100% ~ {}s ~ {}min'.format(
            round(self.recording_duration, 2),
            round(self.recording_duration / 60, 2)
        ), fontsize=10)

        self.save_as_image(self.plt, fig)
        return fig
