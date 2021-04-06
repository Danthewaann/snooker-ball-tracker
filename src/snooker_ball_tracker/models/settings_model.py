import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s

from .settings import BallDetectionTabModel, ColourDetectionTabModel
from snooker_ball_tracker.ball_tracker import BallTracker


class SettingsModel(QtCore.QObject):
    def __init__(self):
        """Creates an instance of this class that contains all of the settings
        used by the ball tracker"""
        super().__init__()
        self._ball_tracker = BallTracker()
        self.models = {
            "colour_detection": ColourDetectionTabModel(),
            "ball_detection": BallDetectionTabModel()
        }

    @property
    def ball_tracker(self) -> BallTracker:
        return self._ball_tracker
