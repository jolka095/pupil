from player_settings.plugins.helpers.plots.Plot import Plot
from player_settings.plugins.helpers.properties.properties import not_defined_area


class HeatmapPlot(Plot):

    def __init__(self, image_path, surfaces_dict, properties):
        super().__init__(image_path, surfaces_dict, properties)
        self.title = properties.heatmaps_plot_title
        self.description = properties.heatmaps_description
        self.fontsize = 12

    def get_heatmap_data_from_surfaces(self, surface_name):
        is_data_valid = True
        surface_width = None  # scaled_pos_x / norm_pos_x
        surface_height = None  # scaled_pos_y / norm_pos_y

        print(f"[surface {surface_name}] Get data to create heatmap")
        xs = self.surfaces_dict[surface_name].get_gaze_points_x_list()
        ys = self.surfaces_dict[surface_name].get_gaze_points_y_list()

        if surface_width is None and surface_height is None:
            try:
                x_normalized = self.surfaces_dict[surface_name].get_normalized_gaze_points_x_list()[0]
                y_normalized = self.surfaces_dict[surface_name].get_normalized_gaze_points_y_list()[0]
                surface_width, surface_height = xs[0] / x_normalized, ys[0] / y_normalized
            except IndexError:
                print(f"WARNING: not found normalized data for {surface_name}")
                x_normalized, y_normalized, surface_width, surface_height = 0, 0, 0, 0
                is_data_valid = False
        xs.append(surface_width)
        ys.append(surface_height)
        print(f"Surface width: {surface_width}, height: {surface_height}")
        return is_data_valid, xs, ys

    def create(self):
        labels_dict = {}
        for key in self.surfaces_dict.keys():
            if key != not_defined_area:
                labels_dict[key] = self.surfaces_dict[key]
        labels = list(labels_dict)

        valid_surfaces_count = 0
        valid_labels = []
        for i, surface_name in enumerate(labels):
            is_data_valid, xs, ys = self.get_heatmap_data_from_surfaces(surface_name)
            if is_data_valid:
                valid_surfaces_count += 1
                valid_labels.append(surface_name)

        fig, ax = self.plt.subplots(nrows=valid_surfaces_count, figsize=(8.27, 9.00))

        for i, surface_name in enumerate(valid_labels):
            is_data_valid, xs, ys = self.get_heatmap_data_from_surfaces(surface_name)

            try:
                heatmap = ax[i]
            except Exception:
                heatmap = ax

            heatmap.set_title(surface_name, fontdict={'fontsize': 7}, loc="right")
            heatmap.hist2d(xs, ys, bins=15)
            heatmap.imshow(
                X=[xs, ys],
                interpolation='nearest',
                cmap='viridis'
            )

        self.save_as_image(self.plt, fig)
        return fig
