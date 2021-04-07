import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s

from .settings import BallDetectionSettings, ColourDetectionSettings
from snooker_ball_tracker.ball_tracker import BallTracker


class Settings(QtCore.QObject):
    def __init__(self):
        """Creates an instance of this class that contains all of the settings
        used by the ball tracker"""
        super().__init__()
        self.models = {
            "colour_detection": ColourDetectionSettings(),
            "ball_detection": BallDetectionSettings()
        }
