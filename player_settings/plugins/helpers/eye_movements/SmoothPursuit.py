from player_settings.plugins.helpers.eye_movements.BasicEyeMovement import BasicEyeMovement


class SmoothPursuit(BasicEyeMovement):

    def __init__(self, dictionary):
        super().__init__(dictionary)
