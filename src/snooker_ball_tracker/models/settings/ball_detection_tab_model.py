from collections import OrderedDict

import PyQt5.QtCore as QtCore

from .ball_detection_setting_model import BallDetectionSettingModel


class BallDetectionTabModel(QtCore.QObject):
    def __init__(self):
        """Creates and instance of this class that contains ball detection 
        properties used by the ball tracker"""
        super().__init__()
        self.models = OrderedDict([
            ("convexity", BallDetectionSettingModel("convexity")),
            ("inertia", BallDetectionSettingModel("inertia")),
            ("circularity", BallDetectionSettingModel("circularity")),
            ("area", BallDetectionSettingModel("area", multiplier=1))
        ])
