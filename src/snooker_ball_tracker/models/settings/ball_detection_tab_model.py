from collections import OrderedDict

import PyQt5.QtCore as QtCore

from .ball_detection_setting_model import BallDetectionSettingModel


class BallDetectionTabModel(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.models = OrderedDict([
            ("convexity", BallDetectionSettingModel("convexity")),
            ("inertia", BallDetectionSettingModel("inertia")),
            ("circularity", BallDetectionSettingModel("circularity")),
            ("area", BallDetectionSettingModel("area", multiplier=1))
        ])
