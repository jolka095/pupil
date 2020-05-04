class GazePoint(object):
    """
    For heatmaps creation.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return float(self.x)

    def get_y(self):
        return float(self.y)
