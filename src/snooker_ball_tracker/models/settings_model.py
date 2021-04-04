from .ball_detection_model import BallDetectionTabModel
from .colour_detection_model import ColourDetectionTabModel

import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s


class SettingsModel(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.models = {
            "colour_detection": ColourDetectionTabModel(),
            "ball_detection": BallDetectionTabModel()
        }



