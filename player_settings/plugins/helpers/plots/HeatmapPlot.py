from player_settings.plugins.helpers.plots.Plot import Plot
from player_settings.plugins.helpers.properties.properties import not_defined_area


class HeatmapPlot(Plot):

    def __init__(self, image_path, surfaces_dict, properties):
        super().__init__(image_path, surfaces_dict, properties)
        self.title = properties.heatmaps_plot_title
        self.description = properties.heatmaps_description
        self.fontsize = 12

    def create(self):
        labels = list(self.surfaces_dict.keys())
        fig, ax = self.plt.subplots(nrows=len(labels) - 1, figsize=(8.27, 9.00))

        surface_width = None  # scaled_pos_x / norm_pos_x
        surface_height = None  # scaled_pos_y / norm_pos_y

        for i, surface_name in enumerate(labels):
            if surface_name != not_defined_area:

                print("Generationg heatmap for surface {}".format(surface_name))
                xs = self.surfaces_dict[surface_name].get_gaze_points_x_list()
                ys = self.surfaces_dict[surface_name].get_gaze_points_y_list()

                if surface_width is None and surface_height is None:
                    x_normalized = self.surfaces_dict[surface_name].get_normalized_gaze_points_x_list()[0]
                    y_normalized = self.surfaces_dict[surface_name].get_normalized_gaze_points_y_list()[0]

                    surface_width = xs[0] / x_normalized
                    surface_height = ys[0] / y_normalized

                xs.append(surface_width)
                ys.append(surface_height)

                ax[i].set_title(surface_name, fontdict={'fontsize': 7}, loc="right")
                ax[i].hist2d(xs, ys, bins=15)
                ax[i].imshow(
                    X=[xs, ys],
                    interpolation='nearest',
                    cmap='viridis'
                )
                print("Surface width: {}, height: {}".format(surface_width, surface_height))
                surface_width, surface_height = None, None
        self.save_as_image(self.plt, fig)
        return fig
