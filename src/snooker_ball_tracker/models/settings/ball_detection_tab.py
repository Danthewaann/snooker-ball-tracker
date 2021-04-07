from collections import OrderedDict
from copy import deepcopy

import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s

from .ball_detection_setting import BallDetectionSettingModel


class BallDetectionTabModel(QtCore.QObject):
    def __init__(self):
        """Creates and instance of this class that contains ball detection 
        properties used by the ball tracker"""
        super().__init__()
        self._blob_detector = deepcopy(s.BLOB_DETECTOR)
        self.models = OrderedDict([
            ("convexity", BallDetectionSettingModel("convexity")),
            ("inertia", BallDetectionSettingModel("inertia")),
            ("circularity", BallDetectionSettingModel("circularity")),
            ("area", BallDetectionSettingModel("area", multiplier=1))
        ])

    @property
    def blob_detector(self) -> dict:
        """Copy of blob detector values loaded from settings

        :return: blob detector
        :rtype: dict
        """
        return self._blob_detector

    @blob_detector.setter
    def blob_detector(self, value: dict):
        """Blob detector setter

        :param value: value to set
        :type value: dict
        """
        self._blob_detector = value
        for model in self.models:
            self.models[model].update(self._blob_detector)
